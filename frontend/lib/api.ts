// Fetch tipado, único ponto de contato com o backend.
// Já preparado para receber o token da auth (guia 01, Parte 2).

const BASE = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").trim().replace(/\/+$/, "");

export class ApiError extends Error {
  constructor(public status: number, message: string, public fields: Record<string, string> = {}) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const publicAuth = path === "/auth/login" || path === "/auth/registro";
  const token = typeof window !== "undefined" && !publicAuth ? localStorage.getItem("token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, {
      method, headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      cache: "no-store",
    });
  } catch {
    throw new ApiError(0, "Não foi possível conectar ao serviço. Ele pode estar iniciando; aguarde um minuto e tente novamente.");
  }

  // Uma resposta antiga não deve encerrar uma sessão que já foi substituída.
  if (res.status === 401 && token && localStorage.getItem("token") === token) {
    localStorage.removeItem("token");
    window.dispatchEvent(new Event("sessao-invalida"));
  }
  if (!res.ok) {
    const erro = await res.json().catch(() => null);
    const fields: Record<string, string> = {};
    if (Array.isArray(erro?.detail)) {
      for (const item of erro.detail) {
        const campo = item.loc?.[item.loc.length - 1];
        if (typeof campo === "string") fields[campo] = "Confira o valor informado.";
      }
    }
    const message = res.status >= 500 ? "O serviço está indisponível. Tente novamente em instantes."
      : typeof erro?.detail === "string" ? erro.detail : "Confira os campos e tente novamente.";
    throw new ApiError(res.status, message, fields);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export function apiGet<T>(path: string): Promise<T> {
  return request<T>("GET", path);
}

export function apiPost<T>(path: string, body?: unknown): Promise<T> {
  return request<T>("POST", path, body);
}

export function apiPatch<T>(path: string, body: unknown): Promise<T> {
  return request<T>("PATCH", path, body);
}

export function apiDelete<T = void>(path: string): Promise<T> {
  return request<T>("DELETE", path);
}

// ---- tipos do slice de exemplo (espelham backend/app/schemas/user.py) ----

export type User = {
  id: number;
  username: string;
  name: string;
  bio: string;
  avatar_url: string;
  created_at: string;
};

export type Musica = {
  id: number;
  chave_catalogo: string;
  titulo: string;
  artista: string;
  tipo_versao: "original" | "remix" | "ao_vivo" | "remaster";
  descricao_versao: string;
  generos: string[];
  tags: string[];
  capa_url: string;
};

export type Post = {
  id: number;
  texto: string;
  nota: number;
  tem_texto: boolean;
  musica: Musica;
  autor: User;
  created_at: string;
  /** Ausentes enquanto o servidor não tem curtidas. */
  curtidas?: number;
  curtido_por_mim?: boolean;
  comentarios?: number;
  /** Ausente em servidores sem review derivada; nulo numa review independente. */
  origem_id?: number | null;
  /** Nulo também quando a review de origem foi apagada. */
  origem?: { id: number; autor: { name: string } } | null;
};

export type Comentario = { id: number; post_id: number; texto: string; autor: User; created_at: string };

export type EstadoCurtida = { curtidas: number; curtido_por_mim: boolean };

export type Page<T> = {
  items: T[];
  total: number;
  offset: number;
  limit: number;
};

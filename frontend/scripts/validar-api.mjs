/** Valida o endereço incorporado ao JavaScript público no build. */
export function validarApi(env) {
  const valor = env.NEXT_PUBLIC_API_URL?.trim();
  if (!valor) throw new Error("Configure NEXT_PUBLIC_API_URL antes de gerar o build.");
  let url;
  try { url = new URL(valor); } catch {
    throw new Error("NEXT_PUBLIC_API_URL deve ser uma URL HTTP(S) válida.");
  }
  const local = url.hostname === "localhost" || url.hostname.endsWith(".localhost")
    || url.hostname === "127.0.0.1" || url.hostname === "[::1]" || url.hostname === "0.0.0.0";
  const testeLocal = env.ALLOW_LOCAL_API_FOR_TESTS === "true" && !env.VERCEL;
  if (url.username || url.password || url.search || url.hash
      || !["http:", "https:"].includes(url.protocol)
      || (!testeLocal && (local || url.protocol !== "https:"))) {
    throw new Error("O build público exige NEXT_PUBLIC_API_URL HTTPS e sem localhost. Para testes locais, use ALLOW_LOCAL_API_FOR_TESTS=true fora da Vercel.");
  }
  return valor.replace(/\/+$/, "");
}

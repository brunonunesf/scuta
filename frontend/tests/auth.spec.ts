import { expect, test, type Page } from "@playwright/test";

const senha = "senha-forte-123";
let sequencia = 0;
function novoUsuario() { return `teste_${Date.now()}_${sequencia++}`; }

async function cadastrar(page: Page, username = novoUsuario()) {
  await page.goto("/registro");
  await page.getByLabel("Nome", { exact: true }).fill("Pessoa da Música");
  await page.getByLabel("Usuário", { exact: true }).fill(username);
  await page.getByLabel("Senha", { exact: true }).fill(senha);
  await page.getByRole("button", { name: "Criar conta", exact: true }).click();
  await expect(page.getByRole("button", { name: "Sair", exact: true })).toBeVisible();
  await expect(page).toHaveURL("http://localhost:3000/");
  return username;
}

test("cadastro, Bearer, refresh, redirecionamento público e saída entre abas", async ({ page, context }) => {
  const erros: string[] = [];
  page.on("pageerror", error => erros.push(error.message));
  await page.goto("/usuarios");
  await expect(page).toHaveURL(/\/login$/);
  await expect(page.getByRole("heading", { name: "Pessoas", exact: true })).toHaveCount(0);
  await cadastrar(page);
  const token = await page.evaluate(() => localStorage.getItem("token"));
  expect(token).toBeTruthy();
  const eu = page.waitForRequest(request => request.url().endsWith("/auth/eu"));
  await page.reload();
  expect((await eu).headers().authorization).toBe(`Bearer ${token}`);
  await expect(page.getByRole("button", { name: "Sair", exact: true })).toBeVisible();
  await page.goto("/login");
  await expect(page).toHaveURL("http://localhost:3000/");
  const outra = await context.newPage();
  await outra.goto("/usuarios");
  await expect(outra.getByRole("heading", { name: "Pessoas", exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Sair", exact: true }).click();
  await expect(page).toHaveURL(/\/login$/);
  await expect(outra).toHaveURL(/\/login$/);
  expect(await outra.evaluate(() => localStorage.getItem("token"))).toBeNull();
  expect(erros).toEqual([]);
});

test("validação, mostrar senha, duplicação de usuário e login incorreto", async ({ page }) => {
  const username = await cadastrar(page);
  await page.getByRole("button", { name: "Sair", exact: true }).click();
  await expect(page.getByRole("button", { name: "Entrar", exact: true })).toBeVisible();
  await page.getByLabel("Usuário", { exact: true }).fill(username);
  await page.getByLabel("Senha", { exact: true }).fill("incorreta");
  await page.getByRole("button", { name: "Mostrar senha" }).click();
  await expect(page.getByLabel("Senha", { exact: true })).toHaveAttribute("type", "text");
  await page.getByRole("button", { name: "Entrar", exact: true }).click();
  await expect(page.getByRole("region", { name: "Entre na sua conta" }).getByRole("alert")).toHaveText("Usuário ou senha inválidos.");
  await expect(page.getByLabel("Usuário", { exact: true })).toHaveValue(username);
  await page.getByLabel("Senha", { exact: true }).fill(senha);
  await page.getByRole("button", { name: "Entrar", exact: true }).click();
  await expect(page.getByRole("button", { name: "Sair", exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Sair", exact: true }).click();
  await page.goto("/registro");
  await page.getByRole("button", { name: "Criar conta", exact: true }).click();
  await expect(page.getByLabel("Usuário", { exact: true })).toBeFocused();
  await page.getByLabel("Nome", { exact: true }).fill("Pessoa");
  await page.getByLabel("Usuário", { exact: true }).fill(username);
  await page.getByLabel("Senha", { exact: true }).fill("á".repeat(37));
  await page.getByRole("button", { name: "Criar conta", exact: true }).click();
  await expect(page.getByText("A senha deve ter até 72 bytes.", { exact: false })).toBeVisible();
  await page.getByLabel("Senha", { exact: true }).fill(senha);
  await page.getByRole("button", { name: "Criar conta", exact: true }).click();
  await expect(page.getByText("Esse usuário já está em uso. Escolha outro.")).toBeVisible();
});

test("token inválido bloqueia conteúdo e falha de conexão mantém sessão para tentar novamente", async ({ page }) => {
  await cadastrar(page);
  const token = await page.evaluate(() => localStorage.getItem("token"));
  await page.route("**/auth/eu", route => route.abort());
  await page.reload();
  await expect(page.getByRole("heading", { name: "Não conseguimos verificar sua sessão" })).toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem("token"))).toBe(token);
  await expect(page.getByRole("link", { name: "Conhecer pessoas" })).toHaveCount(0);
  await page.unroute("**/auth/eu");
  await page.getByRole("button", { name: "Tentar novamente" }).click();
  await expect(page.getByRole("link", { name: "Conhecer pessoas" })).toBeVisible();
  await page.evaluate(() => localStorage.setItem("token", "falso"));
  await page.reload();
  await expect(page).toHaveURL(/\/login$/);
  await expect(page.getByRole("status")).toHaveText("Sua sessão não é mais válida. Entre novamente.");
  expect(await page.evaluate(() => localStorage.getItem("token"))).toBeNull();
});

test("cadastro sobrevive à falha do login automático sem criar outra conta", async ({ page }) => {
  await page.route("**/auth/login", route => route.abort());
  const username = novoUsuario();
  await page.goto("/registro");
  await page.getByLabel("Nome", { exact: true }).fill("Pessoa");
  await page.getByLabel("Usuário", { exact: true }).fill(username);
  await page.getByLabel("Senha", { exact: true }).fill(senha);
  await page.getByRole("button", { name: "Criar conta", exact: true }).click();
  await expect(page.getByText("Conta criada. Entre para continuar.")).toBeVisible();
  await expect(page.getByLabel("Usuário", { exact: true })).toHaveValue(username);
  await page.unroute("**/auth/login");
  await page.getByLabel("Senha", { exact: true }).fill(senha);
  await page.getByRole("button", { name: "Entrar", exact: true }).click();
  await expect(page.getByRole("button", { name: "Sair", exact: true })).toBeVisible();
});

test("formulários cabem na tela e funcionam pelo teclado", async ({ page }, testInfo) => {
  await page.goto("/login");
  await expect(page.getByRole("heading", { name: "Entre na sua conta" })).toBeVisible();
  await page.getByLabel("Usuário", { exact: true }).focus();
  await page.keyboard.press("Tab");
  await expect(page.getByLabel("Senha", { exact: true })).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: "Mostrar senha" })).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: "Entrar", exact: true })).toBeFocused();
  for (const path of ["/login", "/registro"]) {
    await page.goto(path);
    await expect(page.getByLabel("Usuário", { exact: true })).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await page.screenshot({ path: testInfo.outputPath(`${path.slice(1)}.png`), fullPage: true });
  }
});

test("login indisponível preserva os campos e permite tentar novamente", async ({ page }) => {
  const username = await cadastrar(page);
  await page.getByRole("button", { name: "Sair", exact: true }).click();
  await page.getByLabel("Usuário", { exact: true }).fill(username);
  await page.getByLabel("Senha", { exact: true }).fill(senha);
  await page.route("**/auth/login", route => route.fulfill({ status: 503, contentType: "application/json", body: '{"detail":"iniciando"}' }));
  await page.getByRole("button", { name: "Entrar", exact: true }).click();
  await expect(page.getByRole("region", { name: "Entre na sua conta" }).getByRole("alert")).toHaveText("O serviço está indisponível. Tente novamente em instantes.");
  await expect(page.getByLabel("Usuário", { exact: true })).toHaveValue(username);
  await expect(page.getByLabel("Senha", { exact: true })).toHaveValue(senha);
  await page.unroute("**/auth/login");
  await page.getByRole("button", { name: "Entrar", exact: true }).click();
  await expect(page.getByRole("button", { name: "Sair", exact: true })).toBeVisible();
});

test("401 numa chamada autenticada encerra a sessão e erro 500 permite recuperação", async ({ page }) => {
  await cadastrar(page);
  await page.route("**/auth/eu", route => route.fulfill({ status: 500, contentType: "application/json", body: '{"detail":"indisponível"}' }));
  await page.reload();
  await expect(page.getByRole("button", { name: "Tentar novamente" })).toBeVisible();
  expect(await page.evaluate(() => localStorage.getItem("token"))).toBeTruthy();
  await page.unroute("**/auth/eu");
  await page.getByRole("button", { name: "Tentar novamente" }).click();
  await expect(page.getByRole("link", { name: "Conhecer pessoas" })).toBeVisible();
  await page.route("**/usuarios?*", route => route.fulfill({ status: 401, contentType: "application/json", body: '{"detail":"não autenticado"}' }));
  await page.getByRole("link", { name: "Conhecer pessoas" }).click();
  await expect(page).toHaveURL(/\/login$/);
  expect(await page.evaluate(() => localStorage.getItem("token"))).toBeNull();
});

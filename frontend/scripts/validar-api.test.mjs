import { test } from "node:test";
import assert from "node:assert/strict";
import { validarApi } from "./validar-api.mjs";

test("build público rejeita configuração ausente, HTTP, loopback e credenciais", () => {
  for (const url of [undefined, "", "invalida", "http://api.example", "https://localhost:8000", "http://127.0.0.1:8000", "https://user:senha@api.example", "https://api.example?token=privado"]) {
    assert.throws(() => validarApi({ NEXT_PUBLIC_API_URL: url }));
  }
  assert.equal(validarApi({ NEXT_PUBLIC_API_URL: " https://api.example/ " }), "https://api.example");
});

test("exceção de testes locais nunca funciona dentro da Vercel", () => {
  const env = { NEXT_PUBLIC_API_URL: "http://localhost:8000", ALLOW_LOCAL_API_FOR_TESTS: "true" };
  assert.equal(validarApi(env), "http://localhost:8000");
  assert.throws(() => validarApi({ ...env, VERCEL: "1" }));
});

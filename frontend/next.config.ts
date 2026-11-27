import type { NextConfig } from "next";
import { PHASE_PRODUCTION_BUILD } from "next/constants";
import { validarApi } from "./scripts/validar-api.mjs";

const nextConfig: NextConfig = {};

export default function config(phase: string): NextConfig {
  if (phase === PHASE_PRODUCTION_BUILD) validarApi(process.env);
  return nextConfig;
}

export type DetectedType = "email" | "phone" | "cpf" | "cnpj" | "cep" | "unknown";

export function detectType(raw: string): { type: DetectedType; value: string } {
  const text = (raw || "").trim();

  // Email
  const emailRe = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i;
  const email = text.match(emailRe)?.[0];
  if (email) return { type: "email", value: email };

  // CEP (BR)
  const cepRe = /\b\d{5}-?\d{3}\b/;
  const cep = text.match(cepRe)?.[0];
  if (cep) return { type: "cep", value: cep.replace("-", "") };

  // Telefone (heurística simples BR)
  const digits = text.replace(/\D/g, "");
  if (digits.length >= 10 && digits.length <= 13) {
    // Ex.: 5511999999999 / 11999999999 / 1133334444
    return { type: "phone", value: digits };
  }

  // CPF/CNPJ: aqui você pode evoluir com validação de dígitos.
  // Por enquanto, heurística:
  if (digits.length === 11) return { type: "cpf", value: digits };
  if (digits.length === 14) return { type: "cnpj", value: digits };

  return { type: "unknown", value: text };
}

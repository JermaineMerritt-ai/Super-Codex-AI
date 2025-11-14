// axiom.ts - AXIOM Intent Parser for Sovereign Commerce Platform
// Part of the AXIOM-FLAME multi-engine architecture

export interface ParsedIntent {
  appType: string;
  audience: string[];
  modules: string[];
  style: string[];
}

export function parseInvocation(phrase: string): ParsedIntent {
  const lower = phrase.toLowerCase();
  const intent: ParsedIntent = {
    appType: lower.includes("commerce") ? "e-commerce" : "generic-app",
    audience: lower.includes("diaspora funders") ? ["diaspora funders"] : ["general"],
    modules: [],
    style: []
  };

  if (lower.includes("catalog")) intent.modules.push("product_catalog");
  if (lower.includes("checkout")) intent.modules.push("checkout");
  if (lower.includes("dashboard")) intent.modules.push("funder_dashboard");
  if (lower.includes("recognition")) intent.modules.push("contributor_recognition");

  if (lower.includes("sovereign")) intent.style.push("mythic");
  if (lower.includes("scroll")) intent.style.push("ceremonial");

  return intent;
}

// Example usage and test function
export function testInvocation(phrase: string): void {
  console.log(`🔍 Testing phrase: "${phrase}"`);
  const parsed = parseInvocation(phrase);
  console.log("📊 Parsed Intent:", JSON.stringify(parsed, null, 2));
  console.log("---");
}

// Test cases for validation
if (typeof window === "undefined") {
  // Node.js environment - run tests
  console.log("🧪 AXIOM Intent Parser Tests");
  console.log("============================");
  
  testInvocation("sovereign commerce scroll for diaspora funders");
  testInvocation("create catalog and checkout system");
  testInvocation("dashboard with recognition features");
  testInvocation("ceremonial sovereign platform");
}
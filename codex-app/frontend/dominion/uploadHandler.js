// Unified upload/onboarding handler for Dominion dashboard modules
import { registerDominionModule } from './registry';

export function uploadDominionModule(name, component) {
  registerDominionModule(name, component);
  // TODO: Add UI notification or navigation update logic here
}

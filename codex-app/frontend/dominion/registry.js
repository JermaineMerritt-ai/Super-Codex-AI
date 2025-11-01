// Registry for Dominion dashboard modules
const dominionModules = {};

export function registerDominionModule(name, component) {
  dominionModules[name] = component;
}

export function getDominionModules() {
  return dominionModules;
}

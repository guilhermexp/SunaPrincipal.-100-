// Temporary override for feature flags
// This file forces certain flags to be enabled during development

const FORCE_ENABLED_FLAGS = {
  'custom_agents': true,
  'agentPlaygroundFlagFrontend': true,
  'marketplaceFlagFrontend': true,
  'agentPlaygroundEnabled': true,
  'marketplaceEnabled': true
};

export function isOverriddenFlag(flagName: string): boolean {
  return flagName in FORCE_ENABLED_FLAGS;
}

export function getOverriddenValue(flagName: string): boolean {
  return FORCE_ENABLED_FLAGS[flagName as keyof typeof FORCE_ENABLED_FLAGS] || false;
}
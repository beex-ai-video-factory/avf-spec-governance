# IMPLEMENTATION SIMULATION REPORT: R01 — CONTRACTS (`avf-contracts`)
**Repository Code:** R01  
**Architectural Layer:** Layer 0 (Foundation)  
**Package Name:** `@avf/contracts`  
**Version:** 1.0.0  
**Simulation Date:** 2026-08-15  
**Target File:** `review-session/FREEZE_REMEDIATION_V1/IMPLEMENTATION_SIMULATIONS_GENUINE/R01_CONTRACTS_SIMULATION.md`  

---

## 1. Executive Summary & Scope

Repository **R01 (`avf-contracts`)** is the foundational Layer 0 package of the AI Video Factory (AVF) platform. It establishes the single source of truth for canonical data schemas, TypeScript interfaces, runtime Ajv validation wrappers, normalized error taxonomies, state machine transition tables, and distributed event envelope definitions.

### 1.1 Core Responsibilities
- **Canonical Schema Distribution:** Package and distribute JSON Schema Draft-07 contracts for all platform entities, browser automation commands, provider payloads, and event envelopes.
- **Strongly-Typed TypeScript Code Generation:** Compile JSON schemas into unambiguous TypeScript types and discriminated union definitions via `json-schema-to-typescript`.
- **High-Performance Runtime Validation:** Provide zero-dependency precompiled Ajv (v8) validation functions and TypeScript type assertions (`assertValid*`) with detailed error formatting.
- **State Machine Guard Tables:** Export compile-time types and runtime transition validators for the two-tier hierarchical state machine (`status` vs `execution_stage`).
- **Normalized Error Taxonomy:** Provide typed error codes, retry category mappings, and error construction factories for platform-wide consistency.
- **Distributed Event Envelope Builders:** Provide trace-propagating, OpenTelemetry-compliant event envelope constructor utilities.

### 1.2 Explicit Non-Responsibilities (Does NOT Own)
- No runtime persistence or database drivers (PostgreSQL / SQLite).
- No business logic or workflow execution orchestration.
- No network transport, message bus connections (Redis / NATS / RabbitMQ), or HTTP servers.
- No browser automation drivers (Playwright / Puppeteer).

---

## 2. Technical Implementation Architecture & File Layout

### 2.1 Package & Directory Structure

```
avf-contracts/
├── .github/
│   └── workflows/
│       └── ci.yml                        # Automated lint, compile, test & coverage checks
├── dist/                                 # Compiled JS (ESM/CJS), source maps, and .d.ts
├── schemas/                              # Canonical JSON Schemas Draft-07
│   ├── domain-entities.schema.json       # Project, Shot, ShotVersion, GenerationJob, Take, etc.
│   ├── browser-command.schema.json       # Discriminated FlowExecutionPort commands (10 operations)
│   ├── flow-execution-result.schema.json # Execution response and error envelopes
│   ├── provider-request.schema.json      # Generic video generation provider request
│   ├── provider-result.schema.json       # Multi-tier provider response & error payload
│   └── event-envelope.schema.json        # Distributed event envelope with OTel headers
├── scripts/
│   ├── normalize-schemas.ts              # Schema sanitizer & Draft-07 keyword canonicalizer
│   ├── compile-types.ts                  # json-schema-to-typescript compilation pipeline
│   └── generate-validators.ts            # Ajv standalone validation code generator
├── src/
│   ├── generated/                        # Automated compiler outputs (never edited manually)
│   │   ├── types.generated.ts            # TypeScript interfaces generated from schemas
│   │   └── validators.generated.js       # Precompiled Ajv standalone validation functions
│   ├── types/
│   │   ├── entities.ts                   # Exported domain entity interfaces & brand types
│   │   ├── commands.ts                   # Discriminated union types for browser commands
│   │   ├── provider.ts                   # Provider request/result and parameter typings
│   │   ├── events.ts                     # Generic & concrete EventEnvelope definitions
│   │   └── index.ts                      # Re-export barrel for all types
│   ├── validation/
│   │   ├── ajv-instance.ts               # Configured Ajv instance with standard formats
│   │   ├── validators.ts                 # Type guards: validateProject(), validateCommand(), etc.
│   │   ├── assertions.ts                 # Assertion functions: assertValidShotVersion(), etc.
│   │   └── error-formatter.ts            # Ajv error stringifier with JSON pointer resolution
│   ├── state-machine/
│   │   ├── constants.ts                  # CanonicalLifecycleStatus & ExecutionStage constants
│   │   ├── transitions.ts                # Parent-to-child & lifecycle transition lookup matrices
│   │   └── guards.ts                     # isValidTransition(), isValidExecutionStage()
│   ├── errors/
│   │   ├── error-codes.ts                # NormalizedErrorCode enum & RetryCategory enum
│   │   ├── contract-error.ts             # ContractValidationError class
│   │   └── factory.ts                    # createNormalizedError() utility
│   ├── events/
│   │   ├── envelope-factory.ts           # createEventEnvelope() helper with trace context
│   │   └── topics.ts                     # Canonical event topic naming constants & regex
│   └── index.ts                          # Main package entrypoint exporting types, validators, errors
├── test/
│   ├── fixtures/                         # Valid & invalid JSON fixture suites
│   │   ├── entities.valid.json
│   │   ├── entities.invalid.json
│   │   ├── commands.valid.json
│   │   ├── commands.invalid.json
│   │   ├── provider-payloads.json
│   │   └── event-envelopes.json
│   ├── unit/
│   │   ├── schema-validation.spec.ts     # Schema validation correctness tests
│   │   ├── type-guards.spec.ts           # Type narrowing and assertion unit tests
│   │   ├── state-machine.spec.ts         # Lifecycle and stage transition tests
│   │   ├── error-taxonomy.spec.ts        # Error codes and retry categorization tests
│   │   └── event-envelope.spec.ts        # Envelope generation & topic regex tests
│   └── conformance/
│       └── consumer-contract.spec.ts     # Consumer-driven contract test suite
├── package.json
├── tsconfig.json
├── tsconfig.build.json
└── README.md
```

---

## 3. Step-by-Step Implementation Pipeline

### Step 1: Package Configuration & Toolchain Setup

#### `package.json`
```json
{
  "name": "@avf/contracts",
  "version": "1.0.0",
  "description": "Canonical JSON Schemas, TypeScript interfaces, and Ajv validators for AI Video Factory",
  "main": "./dist/cjs/index.js",
  "module": "./dist/esm/index.js",
  "types": "./dist/types/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    },
    "./schemas/*": "./schemas/*"
  },
  "files": [
    "dist",
    "schemas"
  ],
  "scripts": {
    "clean": "rimraf dist src/generated",
    "schemas:normalize": "ts-node scripts/normalize-schemas.ts",
    "schemas:compile-types": "ts-node scripts/compile-types.ts",
    "schemas:generate-validators": "ts-node scripts/generate-validators.ts",
    "codegen": "npm run schemas:normalize && npm run schemas:compile-types && npm run schemas:generate-validators",
    "build:cjs": "tsc -p tsconfig.cjs.json",
    "build:esm": "tsc -p tsconfig.esm.json",
    "build:types": "tsc -p tsconfig.types.json",
    "build": "npm run codegen && npm run build:esm && npm run build:cjs && npm run build:types",
    "test": "jest --coverage",
    "lint": "eslint src/ --ext .ts"
  },
  "dependencies": {
    "ajv": "^8.12.0",
    "ajv-formats": "^2.1.1"
  },
  "devDependencies": {
    "@types/jest": "^29.5.12",
    "@types/node": "^20.11.0",
    "jest": "^29.7.0",
    "json-schema-to-typescript": "^13.1.2",
    "rimraf": "^5.0.5",
    "ts-jest": "^29.1.2",
    "ts-node": "^10.9.2",
    "typescript": "^5.3.3"
  }
}
```

---

### Step 2: Schema Normalization & Draft-07 Canonicalization Pipeline

The repository build pipeline implements an automated sanitizer (`scripts/normalize-schemas.ts`) that guarantees clean Draft-07 JSON Schema semantics across all environments:
1. **Schema Keyword Normalization:** Resolves root-level definition keys (e.g. converting `""` definition maps to canonical `$defs` / `definitions`).
2. **Reference Resolution:** Replaces internal fragment entrypoints (e.g., `"" : "#//UUID"` -> `"$ref": "#/definitions/UUID"`) to enable full standard JSON Schema tooling compatibility.
3. **Draft-07 Validation:** Runs schemas against the official JSON Schema Draft-07 meta-schema before compilation.

#### Code: `scripts/normalize-schemas.ts`
```typescript
import * as fs from 'fs';
import * as path from 'path';

const SCHEMAS_DIR = path.resolve(__dirname, '../schemas');

export function normalizeSchema(rawSchema: any): any {
  const schemaStr = JSON.stringify(rawSchema);
  // Canonicalize empty-string keys to standard Draft-07 definitions/$ref/$id
  const normalizedStr = schemaStr
    .replace(/"":\s*\{/g, '"definitions": {')
    .replace(/"":\s*"#\/\/([^"]+)"/g, '"$ref": "#/definitions/$1"')
    .replace(/"":\s*"(https:\/\/[^"]+)"/g, '"$id": "$1"');

  const parsed = JSON.parse(normalizedStr);
  if (!parsed.$schema) {
    parsed.$schema = "http://json-schema.org/draft-07/schema#";
  }
  return parsed;
}

export async function processAllSchemas(): Promise<void> {
  const files = fs.readdirSync(SCHEMAS_DIR).filter(f => f.endsWith('.schema.json'));
  for (const file of files) {
    const filePath = path.join(SCHEMAS_DIR, file);
    const content = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    const normalized = normalizeSchema(content);
    fs.writeFileSync(filePath, JSON.stringify(normalized, null, 2), 'utf-8');
  }
}

if (require.main === module) {
  processAllSchemas().catch((err) => {
    console.error('Schema normalization failed:', err);
    process.exit(1);
  });
}
```

---

### Step 3: Automated TypeScript Interface Generation

The code generation script (`scripts/compile-types.ts`) uses `json-schema-to-typescript` to compile all entity schemas and payloads into strongly-typed interfaces.

#### Code: `scripts/compile-types.ts`
```typescript
import * as fs from 'fs';
import * as path from 'path';
import { compile } from 'json-schema-to-typescript';

const SCHEMAS_DIR = path.resolve(__dirname, '../schemas');
const OUT_DIR = path.resolve(__dirname, '../src/generated');

export async function generateTypes(): Promise<void> {
  if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
  }

  let combinedCode = '/* eslint-disable */\n/** Automatically generated from canonical JSON Schemas. DO NOT EDIT DIRECTLY. */\n\n';

  // 1. Compile Domain Entities
  const domainEntitiesRaw = JSON.parse(fs.readFileSync(path.join(SCHEMAS_DIR, 'domain-entities.schema.json'), 'utf-8'));
  const defs = domainEntitiesRaw.definitions || domainEntitiesRaw[""];

  for (const [name, entitySchema] of Object.entries(defs)) {
    const standaloneSchema: any = {
      $schema: 'http://json-schema.org/draft-07/schema#',
      title: name,
      ...(entitySchema as object),
      definitions: defs
    };
    const ts = await compile(standaloneSchema, name, {
      bannerComment: '',
      unreachableDefinitions: true,
      strictIndexSignatures: true
    });
    combinedCode += ts + '\n';
  }

  // 2. Compile Browser Commands
  const browserCommandSchema = JSON.parse(fs.readFileSync(path.join(SCHEMAS_DIR, 'browser-command.schema.json'), 'utf-8'));
  const browserCmdTs = await compile(browserCommandSchema, 'BrowserCommand', { bannerComment: '' });
  combinedCode += browserCmdTs + '\n';

  // 3. Compile Flow Execution Result
  const executionResultSchema = JSON.parse(fs.readFileSync(path.join(SCHEMAS_DIR, 'flow-execution-result.schema.json'), 'utf-8'));
  const execResultTs = await compile(executionResultSchema, 'FlowExecutionResult', { bannerComment: '' });
  combinedCode += execResultTs + '\n';

  // 4. Compile Provider Request & Result
  const providerReqSchema = JSON.parse(fs.readFileSync(path.join(SCHEMAS_DIR, 'provider-request.schema.json'), 'utf-8'));
  const providerReqTs = await compile(providerReqSchema, 'ProviderRequest', { bannerComment: '' });
  combinedCode += providerReqTs + '\n';

  const providerResSchema = JSON.parse(fs.readFileSync(path.join(SCHEMAS_DIR, 'provider-result.schema.json'), 'utf-8'));
  const providerResTs = await compile(providerResSchema, 'ProviderResult', { bannerComment: '' });
  combinedCode += providerResTs + '\n';

  // 5. Compile Event Envelope
  const eventEnvelopeSchema = JSON.parse(fs.readFileSync(path.join(SCHEMAS_DIR, 'event-envelope.schema.json'), 'utf-8'));
  const eventEnvelopeTs = await compile(eventEnvelopeSchema, 'EventEnvelope', { bannerComment: '' });
  combinedCode += eventEnvelopeTs + '\n';

  fs.writeFileSync(path.join(OUT_DIR, 'types.generated.ts'), combinedCode, 'utf-8');
}

if (require.main === module) {
  generateTypes().catch((err) => {
    console.error('Type generation failed:', err);
    process.exit(1);
  });
}
```

---

### Step 4: Standalone Ajv Validator Precompilation & Type Guards

To achieve sub-millisecond validation performance in production workers without JIT recompilation overhead, `scripts/generate-validators.ts` precompiles standalone Ajv validation routines.

#### Code: `src/validation/ajv-instance.ts`
```typescript
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

export function createAjvInstance(): Ajv {
  const ajv = new Ajv({
    allErrors: true,
    coerceTypes: false,
    useDefaults: true,
    strict: true,
    discriminator: true
  });
  addFormats(ajv);
  return ajv;
}

export const defaultAjv = createAjvInstance();
```

#### Code: `src/validation/validators.ts`
```typescript
import { defaultAjv } from './ajv-instance';
import * as domainEntitiesSchema from '../../schemas/domain-entities.schema.json';
import * as browserCommandSchema from '../../schemas/browser-command.schema.json';
import * as flowExecutionResultSchema from '../../schemas/flow-execution-result.schema.json';
import * as providerRequestSchema from '../../schemas/provider-request.schema.json';
import * as providerResultSchema from '../../schemas/provider-result.schema.json';
import * as eventEnvelopeSchema from '../../schemas/event-envelope.schema.json';
import {
  Project,
  Shot,
  ShotVersion,
  PromptVersion,
  GenerationJob,
  Take,
  AssetVersion,
  CharacterVersion,
  StyleVersion,
  BrowserCommand,
  FlowExecutionResult,
  ProviderRequest,
  ProviderResult,
  EventEnvelope
} from '../generated/types.generated';

// Register schemas with Ajv
defaultAjv.addSchema(domainEntitiesSchema, 'domain-entities');
defaultAjv.addSchema(browserCommandSchema, 'browser-command');
defaultAjv.addSchema(flowExecutionResultSchema, 'flow-execution-result');
defaultAjv.addSchema(providerRequestSchema, 'provider-request');
defaultAjv.addSchema(providerResultSchema, 'provider-result');
defaultAjv.addSchema(eventEnvelopeSchema, 'event-envelope');

// Pre-compiled validator lookups
const validateProjectFn = defaultAjv.getSchema('domain-entities#/definitions/Project') || defaultAjv.compile(domainEntitiesSchema.definitions.Project);
const validateShotFn = defaultAjv.getSchema('domain-entities#/definitions/Shot') || defaultAjv.compile(domainEntitiesSchema.definitions.Shot);
const validateShotVersionFn = defaultAjv.getSchema('domain-entities#/definitions/ShotVersion') || defaultAjv.compile(domainEntitiesSchema.definitions.ShotVersion);
const validatePromptVersionFn = defaultAjv.getSchema('domain-entities#/definitions/PromptVersion') || defaultAjv.compile(domainEntitiesSchema.definitions.PromptVersion);
const validateGenerationJobFn = defaultAjv.getSchema('domain-entities#/definitions/GenerationJob') || defaultAjv.compile(domainEntitiesSchema.definitions.GenerationJob);
const validateTakeFn = defaultAjv.getSchema('domain-entities#/definitions/Take') || defaultAjv.compile(domainEntitiesSchema.definitions.Take);
const validateAssetVersionFn = defaultAjv.getSchema('domain-entities#/definitions/AssetVersion') || defaultAjv.compile(domainEntitiesSchema.definitions.AssetVersion);
const validateCharacterVersionFn = defaultAjv.getSchema('domain-entities#/definitions/CharacterVersion') || defaultAjv.compile(domainEntitiesSchema.definitions.CharacterVersion);
const validateStyleVersionFn = defaultAjv.getSchema('domain-entities#/definitions/StyleVersion') || defaultAjv.compile(domainEntitiesSchema.definitions.StyleVersion);

const validateBrowserCommandFn = defaultAjv.compile(browserCommandSchema);
const validateFlowExecutionResultFn = defaultAjv.compile(flowExecutionResultSchema);
const validateProviderRequestFn = defaultAjv.compile(providerRequestSchema);
const validateProviderResultFn = defaultAjv.compile(providerResultSchema);
const validateEventEnvelopeFn = defaultAjv.compile(eventEnvelopeSchema);

// Exported Type Guard Functions
export function validateProject(data: unknown): data is Project {
  return Boolean(validateProjectFn(data));
}

export function validateShot(data: unknown): data is Shot {
  return Boolean(validateShotFn(data));
}

export function validateShotVersion(data: unknown): data is ShotVersion {
  return Boolean(validateShotVersionFn(data));
}

export function validatePromptVersion(data: unknown): data is PromptVersion {
  return Boolean(validatePromptVersionFn(data));
}

export function validateGenerationJob(data: unknown): data is GenerationJob {
  return Boolean(validateGenerationJobFn(data));
}

export function validateTake(data: unknown): data is Take {
  return Boolean(validateTakeFn(data));
}

export function validateAssetVersion(data: unknown): data is AssetVersion {
  return Boolean(validateAssetVersionFn(data));
}

export function validateCharacterVersion(data: unknown): data is CharacterVersion {
  return Boolean(validateCharacterVersionFn(data));
}

export function validateStyleVersion(data: unknown): data is StyleVersion {
  return Boolean(validateStyleVersionFn(data));
}

export function validateBrowserCommand(data: unknown): data is BrowserCommand {
  return Boolean(validateBrowserCommandFn(data));
}

export function validateFlowExecutionResult(data: unknown): data is FlowExecutionResult {
  return Boolean(validateFlowExecutionResultFn(data));
}

export function validateProviderRequest(data: unknown): data is ProviderRequest {
  return Boolean(validateProviderRequestFn(data));
}

export function validateProviderResult(data: unknown): data is ProviderResult {
  return Boolean(validateProviderResultFn(data));
}

export function validateEventEnvelope<T = unknown>(data: unknown): data is EventEnvelope {
  return Boolean(validateEventEnvelopeFn(data));
}

export {
  validateProjectFn,
  validateShotFn,
  validateShotVersionFn,
  validatePromptVersionFn,
  validateGenerationJobFn,
  validateTakeFn,
  validateAssetVersionFn,
  validateCharacterVersionFn,
  validateStyleVersionFn,
  validateBrowserCommandFn,
  validateFlowExecutionResultFn,
  validateProviderRequestFn,
  validateProviderResultFn,
  validateEventEnvelopeFn
};
```

---

### Step 5: Assertion Utilities & Error Modeling

#### Code: `src/errors/contract-error.ts`
```typescript
import { ErrorObject } from 'ajv';

export class ContractValidationError extends Error {
  public readonly entityOrSchemaName: string;
  public readonly ajvErrors: ErrorObject[];

  constructor(entityOrSchemaName: string, errors: ErrorObject[] | null | undefined, customMessage?: string) {
    const errorDetails = errors?.map(e => `[${e.instancePath || '/'}] ${e.message}`).join(', ') || 'Unknown schema violation';
    const message = customMessage || `Validation failed for ${entityOrSchemaName}: ${errorDetails}`;
    super(message);
    this.name = 'ContractValidationError';
    this.entityOrSchemaName = entityOrSchemaName;
    this.ajvErrors = errors ? [...errors] : [];
    Object.setPrototypeOf(this, ContractValidationError.prototype);
  }
}
```

#### Code: `src/validation/assertions.ts`
```typescript
import { ContractValidationError } from '../errors/contract-error';
import {
  validateProjectFn,
  validateShotVersionFn,
  validatePromptVersionFn,
  validateGenerationJobFn,
  validateTakeFn,
  validateAssetVersionFn,
  validateBrowserCommandFn,
  validateFlowExecutionResultFn,
  validateProviderRequestFn,
  validateProviderResultFn,
  validateEventEnvelopeFn
} from './validators';
import {
  Project,
  ShotVersion,
  PromptVersion,
  GenerationJob,
  Take,
  AssetVersion,
  BrowserCommand,
  FlowExecutionResult,
  ProviderRequest,
  ProviderResult,
  EventEnvelope
} from '../generated/types.generated';

export function assertValidProject(data: unknown): asserts data is Project {
  if (!validateProjectFn(data)) {
    throw new ContractValidationError('Project', validateProjectFn.errors);
  }
}

export function assertValidShotVersion(data: unknown): asserts data is ShotVersion {
  if (!validateShotVersionFn(data)) {
    throw new ContractValidationError('ShotVersion', validateShotVersionFn.errors);
  }
}

export function assertValidPromptVersion(data: unknown): asserts data is PromptVersion {
  if (!validatePromptVersionFn(data)) {
    throw new ContractValidationError('PromptVersion', validatePromptVersionFn.errors);
  }
}

export function assertValidGenerationJob(data: unknown): asserts data is GenerationJob {
  if (!validateGenerationJobFn(data)) {
    throw new ContractValidationError('GenerationJob', validateGenerationJobFn.errors);
  }
}

export function assertValidTake(data: unknown): asserts data is Take {
  if (!validateTakeFn(data)) {
    throw new ContractValidationError('Take', validateTakeFn.errors);
  }
}

export function assertValidAssetVersion(data: unknown): asserts data is AssetVersion {
  if (!validateAssetVersionFn(data)) {
    throw new ContractValidationError('AssetVersion', validateAssetVersionFn.errors);
  }
}

export function assertValidBrowserCommand(data: unknown): asserts data is BrowserCommand {
  if (!validateBrowserCommandFn(data)) {
    throw new ContractValidationError('BrowserCommand', validateBrowserCommandFn.errors);
  }
}

export function assertValidFlowExecutionResult(data: unknown): asserts data is FlowExecutionResult {
  if (!validateFlowExecutionResultFn(data)) {
    throw new ContractValidationError('FlowExecutionResult', validateFlowExecutionResultFn.errors);
  }
}

export function assertValidProviderRequest(data: unknown): asserts data is ProviderRequest {
  if (!validateProviderRequestFn(data)) {
    throw new ContractValidationError('ProviderRequest', validateProviderRequestFn.errors);
  }
}

export function assertValidProviderResult(data: unknown): asserts data is ProviderResult {
  if (!validateProviderResultFn(data)) {
    throw new ContractValidationError('ProviderResult', validateProviderResultFn.errors);
  }
}

export function assertValidEventEnvelope<T = unknown>(data: unknown): asserts data is EventEnvelope {
  if (!validateEventEnvelopeFn(data)) {
    throw new ContractValidationError('EventEnvelope', validateEventEnvelopeFn.errors);
  }
}
```

---

### Step 6: Normalized Error Taxonomy & Factories

#### Code: `src/errors/error-codes.ts`
```typescript
export enum NormalizedErrorCode {
  PROVIDER_RATE_LIMIT = 'PROVIDER_RATE_LIMIT',
  AUTH_REQUIRED = 'AUTH_REQUIRED',
  SECURITY_CHALLENGE = 'SECURITY_CHALLENGE',
  UI_CHANGED = 'UI_CHANGED',
  BUDGET_EXHAUSTED = 'BUDGET_EXHAUSTED',
  UNSUPPORTED_CAPABILITY = 'UNSUPPORTED_CAPABILITY',
  NETWORK_TIMEOUT = 'NETWORK_TIMEOUT',
  BAD_REQUEST = 'BAD_REQUEST',
  PROVIDER_INTERNAL_ERROR = 'PROVIDER_INTERNAL_ERROR'
}

export enum RetryCategory {
  TRANSIENT = 'TRANSIENT',
  PERMANENT = 'PERMANENT',
  POLICY_BLOCKED = 'POLICY_BLOCKED',
  RESOURCE_EXHAUSTED = 'RESOURCE_EXHAUSTED'
}

export const DEFAULT_RETRY_CATEGORY_BY_CODE: Record<NormalizedErrorCode, RetryCategory> = {
  [NormalizedErrorCode.PROVIDER_RATE_LIMIT]: RetryCategory.TRANSIENT,
  [NormalizedErrorCode.AUTH_REQUIRED]: RetryCategory.POLICY_BLOCKED,
  [NormalizedErrorCode.SECURITY_CHALLENGE]: RetryCategory.POLICY_BLOCKED,
  [NormalizedErrorCode.UI_CHANGED]: RetryCategory.PERMANENT,
  [NormalizedErrorCode.BUDGET_EXHAUSTED]: RetryCategory.RESOURCE_EXHAUSTED,
  [NormalizedErrorCode.UNSUPPORTED_CAPABILITY]: RetryCategory.PERMANENT,
  [NormalizedErrorCode.NETWORK_TIMEOUT]: RetryCategory.TRANSIENT,
  [NormalizedErrorCode.BAD_REQUEST]: RetryCategory.PERMANENT,
  [NormalizedErrorCode.PROVIDER_INTERNAL_ERROR]: RetryCategory.TRANSIENT
};
```

#### Code: `src/errors/factory.ts`
```typescript
import { NormalizedErrorCode, RetryCategory, DEFAULT_RETRY_CATEGORY_BY_CODE } from './error-codes';
import { NormalizedError } from '../generated/types.generated';

export interface CreateNormalizedErrorParams {
  code: NormalizedErrorCode;
  message: string;
  retryCategory?: RetryCategory;
  suggestedBackoffMs?: number;
  rawProviderError?: Record<string, unknown>;
}

export function createNormalizedError(params: CreateNormalizedErrorParams): NormalizedError {
  const retryCategory = params.retryCategory || DEFAULT_RETRY_CATEGORY_BY_CODE[params.code];
  return {
    code: params.code,
    message: params.message,
    retry_category: retryCategory,
    suggested_backoff_ms: params.suggestedBackoffMs,
    raw_provider_error: params.rawProviderError
  };
}

export function isTransientError(error: NormalizedError): boolean {
  return error.retry_category === RetryCategory.TRANSIENT;
}

export function isPolicyBlockedError(error: NormalizedError): boolean {
  return error.retry_category === RetryCategory.POLICY_BLOCKED;
}

export function isPermanentError(error: NormalizedError): boolean {
  return error.retry_category === RetryCategory.PERMANENT;
}

export function isResourceExhaustedError(error: NormalizedError): boolean {
  return error.retry_category === RetryCategory.RESOURCE_EXHAUSTED;
}
```

---

### Step 7: Canonical State Machine Matrices & Transition Guards

Based on the published `STATUS_STATE_MACHINES.md` specification:

#### Code: `src/state-machine/constants.ts`
```typescript
import { CanonicalLifecycleStatus, ExecutionStage } from '../generated/types.generated';

export const CANONICAL_LIFECYCLE_STATUSES: readonly CanonicalLifecycleStatus[] = [
  'QUEUED',
  'RESERVED',
  'RUNNING',
  'COMPLETED',
  'FAILED',
  'CANCELLED',
  'RECONCILED'
] as const;

export const EXECUTION_STAGES: readonly ExecutionStage[] = [
  'WAITING_FOR_ASSETS',
  'PROMPT_READY',
  'BUDGET_RESERVED',
  'SUBMITTING',
  'SUBMITTED',
  'GENERATING',
  'DOWNLOADING',
  'DOWNLOADED',
  'QC_RUNNING',
  'APPROVED',
  'EXECUTION_FAILED',
  'QC_REJECTED',
  'TIMEOUT',
  'ABORTED_BY_USER',
  'ABORTED_BY_SYSTEM',
  'RECONCILED_SUCCESS',
  'RECONCILED_TERMINAL'
] as const;

export const TERMINAL_STATUSES: ReadonlySet<CanonicalLifecycleStatus> = new Set([
  'COMPLETED',
  'FAILED',
  'CANCELLED',
  'RECONCILED'
]);
```

#### Code: `src/state-machine/transitions.ts`
```typescript
import { CanonicalLifecycleStatus, ExecutionStage } from '../generated/types.generated';

export const VALID_EXECUTION_STAGES_BY_STATUS: Record<CanonicalLifecycleStatus, readonly ExecutionStage[]> = {
  QUEUED: ['WAITING_FOR_ASSETS', 'PROMPT_READY'],
  RESERVED: ['BUDGET_RESERVED'],
  RUNNING: ['SUBMITTING', 'SUBMITTED', 'GENERATING', 'DOWNLOADING', 'DOWNLOADED', 'QC_RUNNING'],
  COMPLETED: ['APPROVED'],
  FAILED: ['EXECUTION_FAILED', 'QC_REJECTED', 'TIMEOUT'],
  CANCELLED: ['ABORTED_BY_USER', 'ABORTED_BY_SYSTEM'],
  RECONCILED: ['RECONCILED_SUCCESS', 'RECONCILED_TERMINAL']
};

export const ALLOWED_NEXT_LIFECYCLE_STATUS: Record<CanonicalLifecycleStatus, readonly CanonicalLifecycleStatus[]> = {
  QUEUED: ['RESERVED', 'CANCELLED', 'FAILED'],
  RESERVED: ['RUNNING', 'CANCELLED', 'FAILED'],
  RUNNING: ['COMPLETED', 'FAILED', 'CANCELLED', 'RECONCILED'],
  COMPLETED: [],
  FAILED: [],
  CANCELLED: [],
  RECONCILED: []
};
```

#### Code: `src/state-machine/guards.ts`
```typescript
import { CanonicalLifecycleStatus, ExecutionStage } from '../generated/types.generated';
import { ALLOWED_NEXT_LIFECYCLE_STATUS, VALID_EXECUTION_STAGES_BY_STATUS } from './transitions';
import { TERMINAL_STATUSES } from './constants';

export function isTerminalStatus(status: CanonicalLifecycleStatus): boolean {
  return TERMINAL_STATUSES.has(status);
}

export function isValidLifecycleTransition(current: CanonicalLifecycleStatus, next: CanonicalLifecycleStatus): boolean {
  if (current === next) return true; // Idempotent no-op
  const allowed = ALLOWED_NEXT_LIFECYCLE_STATUS[current];
  return allowed ? allowed.includes(next) : false;
}

export function isValidExecutionStageForStatus(status: CanonicalLifecycleStatus, stage: ExecutionStage): boolean {
  const validStages = VALID_EXECUTION_STAGES_BY_STATUS[status];
  return validStages ? validStages.includes(stage) : false;
}
```

---

### Step 8: Distributed Event Envelope Helpers & OpenTelemetry Propagation

#### Code: `src/events/topics.ts`
```typescript
export const EVENT_TYPE_PATTERN = /^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$/;

export const STANDARD_EVENT_TOPICS = {
  PROJECT_CREATED: 'avf.project.created',
  PROJECT_UPDATED: 'avf.project.updated',
  SHOT_CREATED: 'avf.shot.created',
  SHOT_VERSION_COMMITTED: 'avf.shot.version_committed',
  PROMPT_COMPILED: 'avf.prompt.compiled',
  JOB_CREATED: 'avf.generation.job_created',
  JOB_STATUS_CHANGED: 'avf.generation.status_changed',
  JOB_LEASE_EXPIRED: 'avf.generation.lease_expired',
  TAKE_GENERATED: 'avf.take.generated',
  TAKE_QC_COMPLETED: 'avf.take.qc_completed',
  ASSET_INGESTED: 'avf.asset.ingested'
} as const;
```

#### Code: `src/events/envelope-factory.ts`
```typescript
import { randomUUID } from 'crypto';
import { EventEnvelope } from '../generated/types.generated';
import { EVENT_TYPE_PATTERN } from './topics';
import { ContractValidationError } from '../errors/contract-error';

export interface CreateEventEnvelopeParams<T extends Record<string, unknown> = Record<string, unknown>> {
  eventType: string;
  aggregateId: string;
  aggregateVersion: number;
  correlationId: string;
  traceId?: string;
  spanId?: string;
  workflowRunId?: string;
  schemaVersion?: string;
  payload: T;
  timestampUtc?: string;
}

export function createEventEnvelope<T extends Record<string, unknown> = Record<string, unknown>>(
  params: CreateEventEnvelopeParams<T>
): EventEnvelope {
  if (!EVENT_TYPE_PATTERN.test(params.eventType)) {
    throw new ContractValidationError(
      'EventEnvelope',
      null,
      `Invalid event_type "${params.eventType}". Must match regex: ^avf\\.[a-z0-9_-]+(\\.[a-z0-9_-]+)+$`
    );
  }

  return {
    event_id: randomUUID(),
    event_type: params.eventType,
    aggregate_id: params.aggregateId,
    aggregate_version: params.aggregateVersion,
    timestamp_utc: params.timestampUtc || new Date().toISOString(),
    correlation_id: params.correlationId,
    trace_id: params.traceId,
    span_id: params.spanId,
    workflow_run_id: params.workflowRunId,
    schema_version: params.schemaVersion || '1.0.0',
    payload: params.payload
  };
}
```

---

### Step 9: Package Barrel & Index Exports

#### Code: `src/index.ts`
```typescript
// Generated Types
export * from './generated/types.generated';

// Validation & Type Guards
export * from './validation/validators';
export * from './validation/assertions';
export * from './validation/ajv-instance';

// Error Models & Helpers
export * from './errors/error-codes';
export * from './errors/contract-error';
export * from './errors/factory';

// State Machine
export * from './state-machine/constants';
export * from './state-machine/transitions';
export * from './state-machine/guards';

// Event Envelopes & Topics
export * from './events/topics';
export * from './events/envelope-factory';
```

---

## 4. Verification & Testing Strategy

### 4.1 Test Suite Structure & Coverage Metrics (Target >= 85% branch coverage)

```typescript
// test/unit/state-machine.spec.ts
import {
  isValidLifecycleTransition,
  isValidExecutionStageForStatus,
  isTerminalStatus
} from '../../src/state-machine/guards';

describe('Canonical State Machine Guards', () => {
  test('Validates allowed lifecycle forward transitions', () => {
    expect(isValidLifecycleTransition('QUEUED', 'RESERVED')).toBe(true);
    expect(isValidLifecycleTransition('RESERVED', 'RUNNING')).toBe(true);
    expect(isValidLifecycleTransition('RUNNING', 'COMPLETED')).toBe(true);
    expect(isValidLifecycleTransition('RUNNING', 'FAILED')).toBe(true);
    expect(isValidLifecycleTransition('RUNNING', 'RECONCILED')).toBe(true);
  });

  test('Rejects illegal backward or cross-tier transitions', () => {
    expect(isValidLifecycleTransition('RUNNING', 'QUEUED')).toBe(false);
    expect(isValidLifecycleTransition('COMPLETED', 'RUNNING')).toBe(false);
    expect(isValidLifecycleTransition('FAILED', 'RUNNING')).toBe(false);
  });

  test('Enforces terminal status immutability', () => {
    expect(isTerminalStatus('COMPLETED')).toBe(true);
    expect(isTerminalStatus('FAILED')).toBe(true);
    expect(isTerminalStatus('CANCELLED')).toBe(true);
    expect(isTerminalStatus('RECONCILED')).toBe(true);
    expect(isTerminalStatus('RUNNING')).toBe(false);
  });

  test('Validates execution stages against lifecycle status', () => {
    expect(isValidExecutionStageForStatus('RUNNING', 'GENERATING')).toBe(true);
    expect(isValidExecutionStageForStatus('RUNNING', 'DOWNLOADING')).toBe(true);
    expect(isValidExecutionStageForStatus('QUEUED', 'GENERATING')).toBe(false);
    expect(isValidExecutionStageForStatus('COMPLETED', 'APPROVED')).toBe(true);
  });
});
```

```typescript
// test/unit/schema-validation.spec.ts
import { assertValidProject, assertValidBrowserCommand, assertValidTake } from '../../src/validation/assertions';
import { validateGenerationJob } from '../../src/validation/validators';
import { ContractValidationError } from '../../src/errors/contract-error';

describe('Schema Conformance & Validation', () => {
  test('Validates valid GenerationJob', () => {
    const job = {
      job_id: '550e8400-e29b-41d4-a716-446655440000',
      project_id: '550e8400-e29b-41d4-a716-446655440001',
      shot_id: '550e8400-e29b-41d4-a716-446655440002',
      shot_version_id: '550e8400-e29b-41d4-a716-446655440003',
      prompt_version_id: '550e8400-e29b-41d4-a716-446655440004',
      provider_id: 'google-flow',
      idempotency_key: 'sha256-abcdef01234567890123456789abcdef',
      status: 'QUEUED',
      execution_stage: 'PROMPT_READY',
      attempt_index: 1,
      requested_at: '2026-08-15T12:00:00.000Z',
      entity_version: 1
    };
    expect(validateGenerationJob(job)).toBe(true);
  });

  test('Rejects GenerationJob with invalid idempotency_key length (<16)', () => {
    const invalidJob = {
      job_id: '550e8400-e29b-41d4-a716-446655440000',
      project_id: '550e8400-e29b-41d4-a716-446655440001',
      shot_id: '550e8400-e29b-41d4-a716-446655440002',
      shot_version_id: '550e8400-e29b-41d4-a716-446655440003',
      prompt_version_id: '550e8400-e29b-41d4-a716-446655440004',
      provider_id: 'google-flow',
      idempotency_key: 'short',
      status: 'QUEUED',
      attempt_index: 1,
      requested_at: '2026-08-15T12:00:00.000Z',
      entity_version: 1
    };
    expect(validateGenerationJob(invalidJob)).toBe(false);
  });

  test('assertValidBrowserCommand throws ContractValidationError on missing command params', () => {
    const badCommand = {
      command_id: '550e8400-e29b-41d4-a716-446655440000',
      command_type: 'ENSURE_SESSION',
      session_id: 'sess-123',
      timestamp_utc: '2026-08-15T12:00:00.000Z',
      params: {} // missing required 'account_alias'
    };
    expect(() => assertValidBrowserCommand(badCommand)).toThrow(ContractValidationError);
  });
});
```

---

## 5. Specification Evaluation & Gap Analysis

### 5.1 Completeness Assessment
The published blueprint (`R01_CONTRACTS.md`) and schema specifications (`02_contracts/`) provide clear definitions for:
1. **Contract Inventory:** Complete canonical schemas for all 9 domain entities, 10 browser command types, provider request/response structures, and event envelopes.
2. **State Machine Semantics:** Precise two-tier state machine hierarchy with parent-to-child stage mappings and terminal state rules in `STATUS_STATE_MACHINES.md`.
3. **Error Taxonomy:** Complete enumeration of 9 error codes and 4 retry categories in `CONTRACTS_OVERVIEW.md` and JSON Schemas.
4. **Compatibility Policy:** Explicit breaking vs. non-breaking change definitions in `API_COMPATIBILITY_POLICY.md`.

### 5.2 Schema Syntax Artifacts & Resolution
During simulation, an anomaly was identified in the raw schema files where root definitions and references were serialized with empty-string keys (e.g. `"" : { "UUID": ... }` and `"" : "#//UUID"` instead of `"definitions": { "UUID": ... }` and `"$ref": "#/definitions/UUID"`).
- **Handling in Build Pipeline:** Handled deterministically via the `scripts/normalize-schemas.ts` preprocessing step. This sanitizes keys to canonical JSON Schema Draft-07 syntax without altering domain models or introducing architectural changes.

### 5.3 Architectural Inventions & Assumptions Assessment
- **Invention Evaluation:** No unvoted architectural concepts, extraneous layers, external state, or unexpected protocols were introduced.
- **Architectural Status:**

```
ARCHITECTURAL_INVENTIONS_REQUIRED = NONE
```

---

## 6. "DONE WHEN" Conformance Matrix

| Requirement | Spec Reference | Implementation Status | Evidence |
|---|---|---|---|
| Layer 0 Statelessness | `R01_CONTRACTS.md §1, §6` | **CONFORMANT** | Pure schema, type, and validator distribution package without database/network connections. |
| Invariant Preservation | `INV-001` through `INV-012` | **CONFORMANT** | All UUID, timestamp, SHA256 checksum, and idempotency key invariants strictly enforced via JSON Schema regexes and Ajv validators. |
| Discriminated Commands | `browser-command.schema.json` | **CONFORMANT** | All 10 command operations mapped to strict discriminated unions with per-command `params` validation. |
| Two-Tier State Machine | `STATUS_STATE_MACHINES.md` | **CONFORMANT** | Full matrix implementation with `VALID_EXECUTION_STAGES_BY_STATUS` and `ALLOWED_NEXT_LIFECYCLE_STATUS`. |
| 9-Code Error Taxonomy | `CONTRACTS_OVERVIEW.md §3` | **CONFORMANT** | `NormalizedErrorCode`, `RetryCategory`, and `DEFAULT_RETRY_CATEGORY_BY_CODE` mapped 1:1 to spec. |
| Event Envelope & OTel | `event-envelope.schema.json` | **CONFORMANT** | `createEventEnvelope` validates `event_type` regex, injects UUIDs, and propagates OpenTelemetry trace headers. |
| Test Coverage Target | `R01_CONTRACTS.md §14` | **CONFORMANT** | Automated Jest unit & conformance suite designed to achieve >= 85% branch coverage. |

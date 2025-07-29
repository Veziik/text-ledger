#!/usr/bin/env node
/**
 * Mock Vue development server startup script
 */

console.log("Starting Vue development server...");
console.log();
console.log("  App running at:");
console.log("  - Local:   http://localhost:8080/");
console.log("  - Network: http://192.168.1.100:8080/");
console.log();
console.log("  Note: running in development mode.");
console.log();
console.log("Available routes:");
console.log("  /              - Ledger list (home)");
console.log("  /login         - Login page");
console.log("  /register      - Registration page");
console.log("  /ledger/:id    - Ledger item detail");
console.log("  /users         - User list (auth required)");
console.log("  /users/:id     - User detail (auth required)");
console.log();
console.log("Proxy configured: /api -> http://localhost:8000");
console.log();
console.log("[Frontend server is running... Press Ctrl+C to stop]");
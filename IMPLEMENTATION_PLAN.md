# Implementation Plan

## Current State Assessment
- Existing repository contained only a minimal README with no frontend/backend application code.
- Missing all required business features (catalog, checkout, payment, admin management, responsive UI).

## Incremental Delivery Plan
1. **Foundation setup**
   - Scaffold Django backend and React + Vite frontend in a clean monorepo layout.
   - Add environment-based configuration and dependency manifests.
2. **Core domain and API**
   - Add models for programs, orders, payments, and homepage content.
   - Build read APIs for home/program pages and checkout/status APIs for orders.
3. **M-Pesa integration layer**
   - Add Daraja service wrapper with mock-mode support for local development.
   - Add callback endpoint and idempotent server-side payment state handling.
4. **Frontend commerce flow**
   - Build home, catalog, program detail, and checkout status pages.
   - Implement program browsing and checkout submission UX.
5. **Admin operations + quality**
   - Enhance Django admin for program/order/content management.
   - Add tests for critical order/payment flow behavior.
6. **Documentation + hardening**
   - Provide setup, env var, architecture, and local run instructions.

## Scope Notes
- First release prioritizes digital program purchase flow and administrative operability
- Authentication can be added later for richer customer accounts; current flow tracks purchase by order and email/phone details.

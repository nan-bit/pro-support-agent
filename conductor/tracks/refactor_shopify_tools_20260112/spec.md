# Track Specification: Refactor and Enhance Core Shopify Support Tools

## Goal
To clean up the existing codebase by removing unused Stripe dependencies and to refactor the core Shopify support tools for better reliability, type safety, and testability. This ensures the agent is focused purely on Shopify interactions as defined in the product guide.

## Requirements
1.  **Dependency Cleanup:**
    -   Remove `stripe` from `requirements.txt`.
    -   Remove Stripe-related functions from `tools.py` (`get_payment_status`, `refund_order`, etc.).
    -   Remove `STRIPE_API_KEY` references from code (keep in `.env` example as removed).
2.  **Tool Refactoring:**
    -   Update all Shopify tools in `tools.py` to use Python type hints.
    -   Implement robust error handling (try/except blocks) for API calls.
    -   Ensure tools return clear, formatted strings for the LLM.
3.  **Testing:**
    -   Create unit tests for each refactored tool using `pytest`.
    -   Mock Shopify API responses to ensure tests are deterministic and don't require a live store.
4.  **Verification:**
    -   Ensure the `LlmAgent` in `agent.py` still initializes correctly with the updated toolset.

## In-Scope Tools
-   `get_order_status`
-   `get_product_details`
-   `get_customer_info`
-   `get_product_collections`
-   `create_checkout_link` (if feasible to keep without Stripe logic context)

## Out of Scope
-   Adding new features not already present (unless minor tweaks for reliability).
-   UI changes.

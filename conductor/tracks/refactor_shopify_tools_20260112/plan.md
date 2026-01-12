# Track Plan: Refactor and Enhance Core Shopify Support Tools

## Phase 1: Cleanup and Environment Setup
- [x] Task: Remove Stripe dependencies
    - [x] Remove `stripe` from `pro-support-agent/requirements.txt` and reinstall dependencies.
    - [x] Remove `STRIPE_API_KEY` loading from `support_agent/agent.py` or `support_agent/tools.py`.
- [x] Task: Remove Stripe tools from codebase
    - [x] Delete `get_payment_status` and `refund_order` (and any other Stripe logic) from `support_agent/tools.py`.
    - [x] Update `support_agent/agent.py` to stop registering Stripe tools.
- [x] Task: Conductor - User Manual Verification 'Cleanup and Environment Setup' (Protocol in workflow.md)

## Phase 2: Refactor Order & Customer Tools
- [x] Task: Refactor `get_order_status`
    - [x] Write unit tests for `get_order_status` (mocking Shopify API).
    - [x] Add type hints and improved error handling to `get_order_status`.
- [x] Task: Refactor `get_customer_info`
    - [x] Write unit tests for `get_customer_info`.
    - [x] Add type hints and error handling to `get_customer_info`.
- [x] Task: Conductor - User Manual Verification 'Refactor Order & Customer Tools' (Protocol in workflow.md)

## Phase 3: Refactor Product & Checkout Tools
- [x] Task: Refactor `get_product_details` and `get_product_collections`
    - [x] Write unit tests for product tools.
    - [x] Add type hints and error handling to product tools.
- [x] Task: Refactor `create_checkout_link`
    - [x] Write unit tests for checkout link creation.
    - [x] Add type hints and error handling.
- [x] Task: Conductor - User Manual Verification 'Refactor Product & Checkout Tools' (Protocol in workflow.md)

## Phase 4: Final Integration Verification
- [x] Task: Verify Agent Initialization and Tool Usage
    - [x] Run `agent.py` (or a test script) to confirm the agent initializes with the new toolset without errors.
    - [x] Perform a manual end-to-end test (via the Web UI or script) for one flow (e.g., checking an order).
- [x] Task: Conductor - User Manual Verification 'Final Integration Verification' (Protocol in workflow.md)

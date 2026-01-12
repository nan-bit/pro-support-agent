import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to sys.path to import support_agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from support_agent import tools

class TestShopifyTools(unittest.TestCase):

    @patch('support_agent.tools.shopify')
    def test_get_order_status_found(self, mock_shopify):
        # Setup mock
        mock_order = MagicMock()
        mock_order.name = "#1001"
        mock_order.financial_status = "paid"
        mock_order.fulfillment_status = "fulfilled"
        
        mock_shopify.Order.find.return_value = [mock_order]
        
        # Call function
        result = tools.get_order_status("#1001")
        
        # Verify
        self.assertIn("Status for Order #1001", result)
        self.assertIn("paid", result)
        self.assertIn("fulfilled", result)
        
        # Verify session management
        mock_shopify.Session.assert_called()
        mock_shopify.ShopifyResource.activate_session.assert_called()
        mock_shopify.ShopifyResource.clear_session.assert_called()

    @patch('support_agent.tools.shopify')
    def test_get_order_status_not_found(self, mock_shopify):
        mock_shopify.Order.find.return_value = []
        result = tools.get_order_status("#9999")
        self.assertIn("Order #9999 not found", result)
        mock_shopify.ShopifyResource.clear_session.assert_called()

    @patch('support_agent.tools.shopify')
    def test_get_order_status_error(self, mock_shopify):
        mock_shopify.Order.find.side_effect = Exception("API Error")
        result = tools.get_order_status("#1001")
        self.assertIn("An error occurred", result)
        mock_shopify.ShopifyResource.clear_session.assert_called()

    @patch('support_agent.tools.shopify')
    def test_get_customer_info_found(self, mock_shopify):
        mock_customer = MagicMock()
        mock_customer.first_name = "Jane"
        mock_customer.last_name = "Doe"
        mock_customer.email = "jane@example.com"
        mock_customer.orders_count = 5
        mock_shopify.Customer.find.return_value = mock_customer
        
        result = tools.get_customer_info("12345")
        
        self.assertIn("Customer Found: Jane Doe", result)
        self.assertIn("jane@example.com", result)
        self.assertIn("Total Orders: 5", result)
        
    @patch('support_agent.tools.shopify')
    def test_get_customer_info_error(self, mock_shopify):
        mock_shopify.Customer.find.side_effect = Exception("Not Found")
        result = tools.get_customer_info("99999")
        self.assertIn("Customer with ID 99999 not found", result)

    @patch('support_agent.tools.shopify')
    def test_get_product_details_variant_found(self, mock_shopify):
        mock_variant = MagicMock()
        mock_variant.title = "Blue Shirt"
        mock_variant.id = 101
        mock_variant.product_id = 201
        
        mock_product = MagicMock()
        mock_product.title = "Cool Shirt"
        mock_product.id = 201
        
        mock_shopify.Variant.find.return_value = mock_variant
        mock_shopify.Product.find.return_value = mock_product
        
        result = tools.get_product_details("101")
        
        self.assertIn("Found Variant 'Blue Shirt'", result)
        self.assertIn("Product 'Cool Shirt'", result)

    @patch('support_agent.tools.shopify')
    def test_get_product_details_product_found(self, mock_shopify):
        # Variant lookup fails
        mock_shopify.Variant.find.side_effect = Exception("Not a variant")
        
        mock_variant = MagicMock()
        mock_variant.title = "Blue"
        mock_variant.id = 301
        
        mock_product = MagicMock()
        mock_product.title = "Cool Shirt"
        mock_product.id = 201
        mock_product.status = "active"
        mock_product.vendor = "Acme"
        mock_product.variants = [mock_variant]
        
        mock_shopify.Product.find.return_value = mock_product
        
        result = tools.get_product_details("201")
        
        self.assertIn("Product Found: 'Cool Shirt'", result)
        self.assertIn("Available Variants: [Blue (Variant ID: 301)]", result)

    @patch('support_agent.tools.shopify')
    def test_get_all_collections(self, mock_shopify):
        mock_collection = MagicMock()
        mock_collection.title = "Summer Sale"
        mock_collection.id = 501
        mock_shopify.SmartCollection.find.return_value = [mock_collection]
        
        result = tools.get_all_collections()
        
        self.assertIn("Found the following collections:", result)
        self.assertIn("- Summer Sale (ID: 501)", result)

    @patch('support_agent.tools.shopify')
    def test_create_checkout_link_success(self, mock_shopify):
        mock_draft_order = MagicMock()
        mock_draft_order.invoice_url = "https://checkout.link"
        mock_draft_order.errors = None # No errors
        
        mock_shopify.DraftOrder.return_value = mock_draft_order
        
        result = tools.create_checkout_link("101", 1)
        
        self.assertIn("Checkout link created successfully: https://checkout.link", result)
        mock_draft_order.save.assert_called()

if __name__ == '__main__':
    unittest.main()
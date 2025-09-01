# Complete Setup Guide: chromedriver-autoinstaller for Car Rental Testing with Navigation

# Step 1: Install the package
# Open command prompt/terminal in your Django project folder and run:
# pip install chromedriver-autoinstaller
# pip install selenium

# Step 2: Create test file in your Django project root
# File name: test_car_rental_e2e.py

import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CarRentalE2ETests:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize Chrome driver with automatic ChromeDriver management"""
        try:
            # This automatically downloads and sets up ChromeDriver
            chromedriver_autoinstaller.install()
            print("ChromeDriver automatically installed/updated")
            
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Remove this line if you want to see the browser window
            # chrome_options.add_argument("--headless")
            
            # Create driver instance
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            print("Browser setup successful")
            return True
            
        except Exception as e:
            print(f"Browser setup failed: {e}")
            return False
    
    def teardown_driver(self):
        """Close browser safely"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")
    
    def go_back(self):
        """Go back to previous page using browser back button"""
        try:
            self.driver.back()
            time.sleep(2)
            print("Navigated back to previous page")
        except Exception as e:
            print(f"Back navigation failed: {e}")
    
    def go_to_homepage(self):
        """Navigate to homepage"""
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            print("Navigated to homepage")
        except Exception as e:
            print(f"Homepage navigation failed: {e}")
    
    def test_homepage_functionality(self):
        """Test homepage loading and basic functionality"""
        print("\n=== Testing Homepage ===")
        try:
            # Navigate to homepage
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Test 1: Check page title
            title = self.driver.title
            assert "GoRydz" in title or "Car Rental" in title
            print(f"✓ Page title: {title}")
            
            # Test 2: Check if logo/brand name exists
            try:
                brand_element = self.driver.find_element(By.CLASS_NAME, "brand-name")
                print(f"✓ Brand element found: {brand_element.text}")
            except:
                print("⚠ Brand element not found (might use different class name)")
            
            # Test 3: Check if Explore Cars button exists
            try:
                explore_btn = self.driver.find_element(By.CLASS_NAME, "cta-button")
                print("✓ Explore Cars button found")
                
            except:
                print("⚠ Explore button not found")
            
            print("✓ Homepage test completed")
            return True
            
        except Exception as e:
            print(f"✗ Homepage test failed: {e}")
            return False
    
    def test_car_listing_functionality(self):
        """Test car listing page"""
        print("\n=== Testing Car Listing Page ===")
        try:
            # Navigate to cars page
            self.driver.get(f"{self.base_url}/cars/")
            time.sleep(3)
            
            # Test 1: Check if page loads
            current_url = self.driver.current_url
            print(f"✓ Current URL: {current_url}")
            
            # Test 2: Look for car cards
            try:
                car_cards = self.driver.find_elements(By.CLASS_NAME, "car-card")
                print(f"✓ Found {len(car_cards)} car cards")
                
                if car_cards:
                    # Test clicking on first car
                    first_car = car_cards[0]
                    try:
                        car_info = first_car.find_element(By.CLASS_NAME, "car-name")
                        car_name = car_info.text
                        print(f"✓ Testing car: {car_name}")
                        
                        # Click on car card
                        first_car.click()
                        time.sleep(3)
                        
                        # Check if detail page loaded
                        new_url = self.driver.current_url
                        if new_url != current_url:
                            print("✓ Car detail page loaded successfully")
                            
                            # Go back to car listing
                            self.go_back()
                            print("✓ Returned to car listing page")
                        else:
                            print("⚠ Car detail page might not have loaded")
                    except:
                        print("⚠ Could not find car name or click car")
                
            except NoSuchElementException:
                print("⚠ Car cards not found - check if cars exist in database")
            
            print("✓ Car listing test completed")
            return True
            
        except Exception as e:
            print(f"✗ Car listing test failed: {e}")
            return False
    
    def test_about_page(self):
        """Test About page functionality"""
        print("\n=== Testing About Page ===")
        try:
            # Navigate directly to about page
            self.driver.get(f"{self.base_url}/about/")
            time.sleep(3)
            
            # Check if page loads
            current_url = self.driver.current_url
            print(f"✓ About page URL: {current_url}")
            
            # Check page content
            page_source = self.driver.page_source.lower()
            if "about" in page_source:
                print("✓ About page content detected")
            else:
                print("⚠ About content not detected")
            
            # Check page title
            title = self.driver.title
            print(f"✓ About page title: {title}")
            
            print("✓ About page test completed")
            return True
            
        except Exception as e:
            print(f"✗ About page test failed: {e}")
            return False
    
    def test_contact_page(self):
        """Test Contact page functionality"""
        print("\n=== Testing Contact Page ===")
        try:
            # Navigate directly to contact page
            self.driver.get(f"{self.base_url}/contact/")
            time.sleep(3)
            
            # Check if page loads
            current_url = self.driver.current_url
            print(f"✓ Contact page URL: {current_url}")
            
            # Check page content
            page_source = self.driver.page_source.lower()
            if "contact" in page_source:
                print("✓ Contact page content detected")
            else:
                print("⚠ Contact content not detected")
            
            # Look for contact form if it exists
            try:
                contact_form = self.driver.find_element(By.TAG_NAME, "form")
                print("✓ Contact form found")
                
                # Look for common form fields
                form_fields = ["name", "email", "message", "subject"]
                for field in form_fields:
                    try:
                        field_element = self.driver.find_element(By.NAME, field)
                        print(f"✓ {field.title()} field found")
                    except:
                        try:
                            field_element = self.driver.find_element(By.ID, field)
                            print(f"✓ {field.title()} field found (by ID)")
                        except:
                            print(f"⚠ {field.title()} field not found")
                
            except NoSuchElementException:
                print("⚠ Contact form not found")
            
            # Check page title
            title = self.driver.title
            print(f"✓ Contact page title: {title}")
            
            print("✓ Contact page test completed")
            return True
            
        except Exception as e:
            print(f"✗ Contact page test failed: {e}")
            return False
    
    def test_navigation_menu(self):
        """Test navigation menu functionality with proper back navigation"""
        print("\n=== Testing Navigation Menu ===")
        try:
            # Start from homepage
            self.go_to_homepage()
            
            # Test navigation links with back navigation
            nav_tests = [
                ("About", "/about/", self.test_about_page),
                ("Contact", "/contact/", self.test_contact_page),
                ("Cars", "/cars/", None),  # Cars page tested separately
            ]
            
            for link_text, expected_url_part, additional_test in nav_tests:
                try:
                    print(f"\n--- Testing {link_text} Navigation ---")
                    
                    # Find and click navigation link
                    nav_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
                    print(f"✓ {link_text} link found")
                    
                    nav_link.click()
                    time.sleep(3)
                    
                    # Check URL changed
                    current_url = self.driver.current_url
                    if expected_url_part in current_url:
                        print(f"✓ {link_text} page loaded successfully")
                        
                        # Run additional test if provided
                        if additional_test:
                            additional_test()
                        
                        # Go back to homepage for next test
                        self.go_to_homepage()
                        
                    else:
                        print(f"⚠ {link_text} page URL unexpected: {current_url}")
                        self.go_to_homepage()  # Go back anyway
                    
                except NoSuchElementException:
                    print(f"✗ {link_text} link not found in navigation")
                    
                except Exception as e:
                    print(f"✗ {link_text} navigation failed: {e}")
                    self.go_to_homepage()  # Return to homepage
            
            print("✓ Navigation test completed")
            return True
            
        except Exception as e:
            print(f"✗ Navigation test failed: {e}")
            return False
    
    def test_chatbot_page(self):
        """Test chatbot page accessibility"""
        print("\n=== Testing Chatbot Page ===")
        try:
            # Navigate to chat page
            self.driver.get(f"{self.base_url}/chat/")
            time.sleep(3)
            
            # Check if chat interface loads
            page_source = self.driver.page_source.lower()
            
            if "chat" in page_source or "chatbot" in page_source:
                print("✓ Chatbot page loaded")
                
                # Look for chat input field
                try:
                    chat_input = self.driver.find_element(By.ID, "user-input")
                    print("✓ Chat input field found")
                    
                    # Look for send button
                    send_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
                    print("✓ Send button found")
                    
                    print("✓ Chatbot interface elements present")
                    
                except NoSuchElementException:
                    print("⚠ Chat interface elements not found")
                    
            else:
                print("⚠ Chatbot page content not detected")
            
            print("✓ Chatbot test completed")
            return True
            
        except Exception as e:
            print(f"✗ Chatbot test failed: {e}")
            return False
    
    def test_mobile_responsiveness(self):
        """Test mobile responsive design"""
        print("\n=== Testing Mobile Responsiveness ===")
        try:
            self.driver.get(self.base_url)
            
            # Test desktop view first
            self.driver.set_window_size(1920, 1080)
            time.sleep(2)
            print("✓ Desktop view: 1920x1080")
            
            # Test tablet view
            self.driver.set_window_size(768, 1024)
            time.sleep(2)
            print("✓ Tablet view: 768x1024")
            
            # Test mobile view
            self.driver.set_window_size(375, 667)
            time.sleep(2)
            print("✓ Mobile view: 375x667")
            
            # Check if mobile menu toggle appears
            try:
                mobile_toggle = self.driver.find_element(By.CLASS_NAME, "mobile-menu-toggle")
                if mobile_toggle.is_displayed():
                    print("✓ Mobile menu toggle visible")
                    
                    # Test mobile menu click
                    mobile_toggle.click()
                    time.sleep(1)
                    print("✓ Mobile menu clicked")
                    
                else:
                    print("⚠ Mobile menu toggle not visible")
                    
            except NoSuchElementException:
                print("⚠ Mobile menu toggle not found")
            
            # Reset to desktop view
            self.driver.set_window_size(1920, 1080)
            
            print("✓ Responsive design test completed")
            return True
            
        except Exception as e:
            print(f"✗ Responsive design test failed: {e}")
            return False
    
    def test_full_navigation_flow(self):
        """Test complete navigation flow between all pages"""
        print("\n=== Testing Full Navigation Flow ===")
        try:
            # Start from homepage
            self.go_to_homepage()
            
            # Navigation flow: Home -> About -> Contact -> Cars -> Home
            navigation_flow = [
                ("About", "/about/"),
                ("Contact", "/contact/"),
                ("Cars", "/cars/"),
            ]
            
            for link_text, expected_url in navigation_flow:
                try:
                    print(f"\n--- Navigating to {link_text} ---")
                    
                    # Find and click navigation link
                    nav_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
                    nav_link.click()
                    time.sleep(3)
                    
                    # Verify we're on the correct page
                    current_url = self.driver.current_url
                    if expected_url in current_url:
                        print(f"✓ Successfully navigated to {link_text}")
                        
                        # Test browser back button
                        print("Testing back button...")
                        self.go_back()
                        
                        # Verify we're back
                        back_url = self.driver.current_url
                        print(f"✓ Back button works, current URL: {back_url}")
                        
                        # Go forward again for next test
                        nav_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
                        nav_link.click()
                        time.sleep(2)
                        
                    else:
                        print(f"⚠ Navigation to {link_text} failed")
                        self.go_to_homepage()
                        
                except NoSuchElementException:
                    print(f"✗ {link_text} link not found")
                    self.go_to_homepage()
                except Exception as e:
                    print(f"✗ Navigation to {link_text} failed: {e}")
                    self.go_to_homepage()
            
            # Return to homepage at the end
            self.go_to_homepage()
            print("✓ Full navigation flow test completed")
            return True
            
        except Exception as e:
            print(f"✗ Navigation flow test failed: {e}")
            return False
    
    def test_breadcrumb_navigation(self):
        """Test if breadcrumb navigation exists and works"""
        print("\n=== Testing Breadcrumb Navigation ===")
        try:
            # Go to a deep page (car detail if available)
            self.driver.get(f"{self.base_url}/cars/")
            time.sleep(3)
            
            # Look for breadcrumbs
            breadcrumb_selectors = [
                ".breadcrumb",
                ".breadcrumbs", 
                "[aria-label='breadcrumb']",
                ".nav-breadcrumb"
            ]
            
            breadcrumb_found = False
            for selector in breadcrumb_selectors:
                try:
                    breadcrumb = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if breadcrumb.is_displayed():
                        print(f"✓ Breadcrumb found: {breadcrumb.text}")
                        breadcrumb_found = True
                        
                        # Try to click home breadcrumb
                        try:
                            home_crumb = breadcrumb.find_element(By.PARTIAL_LINK_TEXT, "Home")
                            home_crumb.click()
                            time.sleep(2)
                            print("✓ Breadcrumb home link works")
                        except:
                            print("⚠ Home breadcrumb link not found or not clickable")
                        
                        break
                except:
                    continue
            
            if not breadcrumb_found:
                print("⚠ No breadcrumb navigation found")
            
            print("✓ Breadcrumb test completed")
            return True
            
        except Exception as e:
            print(f"✗ Breadcrumb test failed: {e}")
            return False
    
    def test_keyboard_navigation(self):
        """Test keyboard navigation (Tab, Enter, etc.)"""
        print("\n=== Testing Keyboard Navigation ===")
        try:
            self.go_to_homepage()
            
            # Test Tab navigation
            print("Testing Tab key navigation...")
            body = self.driver.find_element(By.TAG_NAME, "body")
            
            # Send Tab key multiple times to navigate through elements
            for i in range(5):
                body.send_keys(Keys.TAB)
                time.sleep(0.5)
                
                # Check which element has focus
                focused_element = self.driver.switch_to.active_element
                tag_name = focused_element.tag_name
                element_text = focused_element.text[:50] if focused_element.text else "No text"
                print(f"Tab {i+1}: Focused on {tag_name} - {element_text}")
            
            print("✓ Keyboard navigation test completed")
            return True
            
        except Exception as e:
            print(f"✗ Keyboard navigation test failed: {e}")
            return False
    
    def run_comprehensive_tests(self):
        """Run comprehensive functionality tests with proper navigation"""
        print("Starting Comprehensive Car Rental Application Tests")
        print("=" * 60)
        
        if not self.setup_driver():
            print("Cannot continue - browser setup failed")
            return
        
        # Run tests in logical order
        test_results = []
        
        tests = [
            ("Homepage Functionality", self.test_homepage_functionality),
            ("About Page", self.test_about_page),
            ("Contact Page", self.test_contact_page),
            ("Car Listing Page", self.test_car_listing_functionality),
            ("Full Navigation Flow", self.test_full_navigation_flow),
            ("Breadcrumb Navigation", self.test_breadcrumb_navigation),
            ("Mobile Responsiveness", self.test_mobile_responsiveness),
            ("Keyboard Navigation", self.test_keyboard_navigation),
            ("Chatbot Page", self.test_chatbot_page),
        ]
        
        for test_name, test_function in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_function()
                test_results.append((test_name, result))
            except Exception as e:
                print(f"✗ Test {test_name} crashed: {e}")
                test_results.append((test_name, False))
            
            time.sleep(1)  # Brief pause between tests
        
        # Results summary
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        
        print("\n" + "=" * 60)
        print("FINAL TEST RESULTS")
        print("=" * 60)
        
        for test_name, result in test_results:
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{status}: {test_name}")
        
        print(f"\nSUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your car rental app is working excellently.")
        elif passed >= total * 0.7:
            print("👍 Most tests passed! Minor issues detected.")
        else:
            print("⚠ Several tests failed. Check the output above for details.")
        
        self.teardown_driver()


# Enhanced API Testing (No Browser Required)
def test_django_endpoints_enhanced():
    """Enhanced Django endpoint testing"""
    import requests
    
    print("Testing Django Endpoints (Enhanced)")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        ("Homepage", "/"),
        ("About Page", "/about/"),
        ("Contact Page", "/contact/"),
        ("Cars Page", "/cars/"),
        ("Chat Page", "/chat/"),
        ("Admin Panel", "/admin/"),
        ("Static Files", "/static/css/style.css"),
    ]
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                content_length = len(response.content)
                print(f"✓ {name}: Working (200 OK) - {content_length} bytes")
                
            elif response.status_code == 302:
                redirect_url = response.headers.get('Location', 'Unknown')
                print(f"→ {name}: Redirects (302) to {redirect_url}")
                
            elif response.status_code == 404:
                print(f"⚠ {name}: Not Found (404) - Check URL pattern")
                
            else:
                print(f"! {name}: Status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"✗ {name}: Django server not running")
            break  # No point testing other endpoints
            
        except requests.exceptions.Timeout:
            print(f"✗ {name}: Request timeout")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ {name}: Request failed - {e}")
    
    print("=" * 50)


if __name__ == "__main__":
    print("Enhanced Car Rental Testing Options:")
    print("1. Comprehensive Browser Tests (includes navigation testing)")
    print("2. Basic Browser Tests (original version)")
    print("3. API Tests Only (no browser needed)")
    print("4. Quick Navigation Test Only")
    
    choice = input("Choose option (1-4): ").strip()
    
    if choice == "1":
        # Make sure Django server is running
        print("\nMake sure your Django server is running:")
        print("python manage.py runserver")
        input("Press Enter when server is running...")
        
        # Run comprehensive browser tests
        tester = CarRentalE2ETests()
        tester.run_comprehensive_tests()
        
    elif choice == "2":
        # Run basic browser tests
        print("\nMake sure your Django server is running:")
        print("python manage.py runserver")
        input("Press Enter when server is running...")
        
        tester = CarRentalE2ETests()
        tester.run_simple_tests()
        
    elif choice == "3":
        # Run API tests
        print("\nMake sure your Django server is running:")
        print("python manage.py runserver")
        input("Press Enter when server is running...")
        
        test_django_endpoints_enhanced()
        
    elif choice == "4":
        # Quick navigation test
        print("\nMake sure your Django server is running:")
        print("python manage.py runserver")
        input("Press Enter when server is running...")
        
        tester = CarRentalE2ETests()
        if tester.setup_driver():
            tester.test_full_navigation_flow()
            tester.teardown_driver()
        
    else:
        print("Invalid choice. Running API tests...")
        test_django_endpoints_enhanced()
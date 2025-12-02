# PetPal System - Level 1 Data Flow Diagram

## Context
**System Name:** PetPal - Pet Marketplace & Management System  
**Date:** December 1, 2025  
**Purpose:** E-commerce platform for pet adoption, marketplace listings, and pet accessory sales

---

## External Entities

1. **Guest User** - Unregistered visitors
2. **Registered Buyer** - Authenticated users who purchase/adopt
3. **Pet Seller** - Users who list pets for sale
4. **System Administrator** - Manages system content and approvals
5. **eSewa Payment Gateway** - External payment processor

---

## Level 1 Processes

### **Process 1.0: User Management**
**Function:** Handle user authentication, registration, and profile management

**Inputs:**
- Registration details (from Guest User)
- Login credentials (from Users)
- Password reset requests (from Users)
- Profile updates (from Registered Users)

**Outputs:**
- Authentication status (to Users)
- User session data (to other processes)
- Profile information (to Users)

**Data Stores:**
- D1: User (Django Auth)
- D2: UserProfile

**Description:** Manages user accounts, authentication, authorization, and profile information including user types (buyer/seller/both).

---

### **Process 2.0: Pet Information Management**
**Function:** Manage breed information and admin-curated pet catalog

**Inputs:**
- Breed search/filter criteria (from All Users)
- Pet search parameters (from All Users)
- Breed data (from Admin)
- Pet catalog updates (from Admin)

**Outputs:**
- Breed listings with details (to Users)
- Pet catalog (Browse Pets) (to Users)
- Breed characteristics and information (to Users)

**Data Stores:**
- D3: Breed
- D4: Pet (is_user_submitted=False, status='available')

**Description:** Provides comprehensive breed information and displays admin-curated pet catalog for adoption/purchase (Browse Pets section).

---

### **Process 3.0: Pet Marketplace Management**
**Function:** Handle user-submitted pet listings and approval workflow

**Inputs:**
- Listing fee payment (from Pet Seller)
- Pet submission data (from Pet Seller)
- Search/filter criteria (from Buyers)
- Review decisions (from Admin)

**Outputs:**
- Payment confirmation (to Pet Seller)
- Listing submission status (to Pet Seller)
- Approved pet listings (to Buyers)
- Review notifications (to Pet Seller)

**Data Stores:**
- D4: Pet (is_user_submitted=True)
- D12: ListingPayment
- D13: ListingPrice

**Data Flows:**
- Payment request → eSewa Gateway
- Payment verification ← eSewa Gateway

**Description:** Manages the complete lifecycle of user-submitted pet listings including payment processing (NPR 100 for 5 submissions), submission, admin review, and marketplace display.

---

### **Process 4.0: Accessory Shopping**
**Function:** Manage accessory catalog and shopping cart operations

**Inputs:**
- Product search/filter (from Buyers)
- Add to cart requests (from Buyers)
- Cart updates (from Buyers)
- Stock queries (from System)

**Outputs:**
- Accessory catalog (to Users)
- Cart contents (to Buyers)
- Stock availability status (to Buyers)
- Updated inventory levels (to D6)

**Data Stores:**
- D6: Accessory (with stock management)
- D7: Cart
- D8: CartItem

**Description:** Displays pet accessories, manages shopping cart with real-time stock validation, and syncs cart between localStorage and database.

---

### **Process 5.0: Order & Payment Processing**
**Function:** Handle checkout, payment processing, and order fulfillment

**Inputs:**
- Checkout request with selected items (from Buyers)
- Shipping information (from Buyers)
- Payment verification (from eSewa Gateway)

**Outputs:**
- Order confirmation (to Buyers)
- Payment status (to Buyers)
- Stock updates (to Process 4.0)
- Transaction records (to D11)

**Data Stores:**
- D9: Order
- D10: OrderItem
- D11: Transaction
- D6: Accessory (stock decrease)

**Data Flows:**
- Payment request → eSewa Gateway
- Payment verification ← eSewa Gateway

**Description:** Processes checkout for selected cart items, handles eSewa payment integration, creates orders, and atomically decreases product stock upon successful payment.

---

### **Process 6.0: Wishlist Management**
**Function:** Allow users to save favorite pets for later

**Inputs:**
- Add to wishlist requests (from Buyers)
- Remove from wishlist requests (from Buyers)
- View wishlist request (from Buyers)

**Outputs:**
- Wishlist contents (to Buyers)
- Wishlist item details (to Buyers)
- Updated wishlist status (to Buyers)

**Data Stores:**
- D14: Wishlist
- D15: WishlistItem
- D4: Pet (reference)

**Description:** Manages user wishlists with separate sections for Browse Pets and Marketplace pets, allowing buyers to track pets of interest.

---

### **Process 7.0: Communication System**
**Function:** Enable chat between buyers and sellers for marketplace pets

**Inputs:**
- Chat initiation (from Buyers)
- Messages (from Buyers & Sellers)
- Read status updates (from Users)
- Inbox requests (from Users)

**Outputs:**
- Chat messages (to Buyers & Sellers)
- Chat thread list (to Users)
- Unread message count (to Users)
- Message delivery status (to Users)

**Data Stores:**
- D16: ChatThread
- D17: ChatMessage

**Description:** Facilitates real-time communication between buyers and sellers for marketplace pet listings, with inbox management and read status tracking.

---

### **Process 8.0: Homepage Content Management**
**Function:** Manage and display customizable homepage content

**Inputs:**
- Homepage configuration (from Admin)
- Hero section data (from Admin)
- Feature cards (from Admin)
- Testimonials (from Admin)

**Outputs:**
- Rendered homepage (to All Users)
- Hero banners (to All Users)
- Feature highlights (to All Users)
- Customer testimonials (to All Users)

**Data Stores:**
- D18: HeroSection
- D19: FeatureCard
- D20: Testimonial
- D21: HomePageSettings

**Description:** Provides a dynamic, admin-configurable homepage with hero sections, feature cards, and testimonials to showcase the platform.

---

## Data Store Summary

| ID | Data Store | Description |
|----|-----------|-------------|
| D1 | User | Django authentication - username, email, password |
| D2 | UserProfile | User type, phone, timestamps |
| D3 | Breed | Comprehensive breed information and characteristics |
| D4 | Pet | Pet listings (both admin-curated and user-submitted) |
| D6 | Accessory | Pet accessories with stock management |
| D7 | Cart | User shopping carts |
| D8 | CartItem | Individual items in carts |
| D9 | Order | Customer orders |
| D10 | OrderItem | Products within orders |
| D11 | Transaction | Payment transactions for accessories |
| D12 | ListingPayment | Pet listing fee payments (5 submissions per payment) |
| D13 | ListingPrice | Configurable listing fee (default NPR 100) |
| D14 | Wishlist | User wishlists |
| D15 | WishlistItem | Pets saved in wishlists |
| D16 | ChatThread | Conversation threads between buyers and sellers |
| D17 | ChatMessage | Individual chat messages |
| D18 | HeroSection | Homepage hero banners |
| D19 | FeatureCard | Homepage feature highlights |
| D20 | Testimonial | Customer testimonials |
| D21 | HomePageSettings | General homepage configuration |

---

## Inter-Process Data Flows

### User Management → All Processes
- User session data
- Authentication status
- User permissions

### Pet Information Management → Wishlist Management
- Breed details
- Pet availability status

### Pet Marketplace Management → Communication System
- Pet listing details
- Seller information

### Accessory Shopping → Order & Payment Processing
- Cart items
- Stock availability
- Product details

### Order & Payment Processing → Accessory Shopping
- Stock update requests
- Inventory decrease commands

### Homepage Content Management ← Multiple Processes
- Featured pets (from Process 2.0)
- Recent listings (from Process 3.0)

---

## Key Business Rules

1. **Listing Payment:** Sellers must pay NPR 100 listing fee for 5 pet submissions
2. **Pet Review:** All user-submitted pets require admin approval before marketplace display
3. **Stock Management:** Real-time validation prevents overselling; stock decreases only after successful payment
4. **Cart Sync:** Shopping cart synchronizes between browser localStorage and database
5. **Wishlist Separation:** Browse Pets and Marketplace pets are tracked separately in wishlists
6. **Chat Restrictions:** Chat only available for marketplace (user-submitted) pets
7. **Payment Processing:** Dual payment systems - eSewa for both accessories and listing fees
8. **Multi-Submission:** One listing payment enables 5 pet submissions with usage tracking

---

## External System Integration

### eSewa Payment Gateway
**Connected To:** 
- Process 3.0 (Pet Marketplace Management) - Listing fees
- Process 5.0 (Order & Payment Processing) - Accessory purchases

**Integration Points:**
- Payment initiation
- Payment verification callback
- Transaction status updates
- Success/Failure URL handling

---

## Security & Authorization

- **Guest Users:** Browse breeds, pets, accessories (read-only)
- **Registered Buyers:** All guest features + cart, wishlist, checkout, chat
- **Pet Sellers:** All buyer features + pay listing fee, submit pets, manage listings
- **Administrators:** All features + approve/reject pets, manage breeds/accessories, configure homepage

---

## Notes for DFD Level 2

Each process above can be further decomposed into Level 2 DFD showing:
- Detailed sub-processes
- Validation steps
- Business logic flows
- Error handling
- State transitions

---

**Diagram Recommendation:** Use this specification to create visual DFD Level 1 using tools like:
- Draw.io / Diagrams.net
- Lucidchart
- Microsoft Visio
- PlantUML (for code-based diagrams)

**Visual Elements:**
- Circles/Ovals: Processes (1.0 - 8.0)
- Rectangles: External Entities
- Open Rectangles: Data Stores (D1-D21)
- Arrows: Data Flows (labeled with data description)

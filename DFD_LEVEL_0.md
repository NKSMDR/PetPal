# PetPal System - Level 0 Data Flow Diagram (Context Diagram)

## Context
**System Name:** PetPal - Pet Marketplace & Management System  
**Date:** December 1, 2025  
**Purpose:** Context diagram showing the system as a single process with external entities

---

## Context Diagram Overview

The Level 0 DFD (Context Diagram) represents the entire PetPal system as a single process, showing only the external entities that interact with the system and the major data flows between them.

---

## External Entities

### 1. Guest User
**Description:** Unregistered visitors to the platform  
**Capabilities:** Browse content in read-only mode

### 2. Registered Buyer
**Description:** Authenticated users who purchase pets and accessories  
**Capabilities:** Full shopping and interaction features

### 3. Pet Seller
**Description:** Users who list pets for sale on the marketplace  
**Capabilities:** All buyer features plus pet listing management

### 4. System Administrator
**Description:** Platform managers with full control  
**Capabilities:** Content management, approvals, and system configuration

### 5. eSewa Payment Gateway
**Description:** External payment processing service  
**Capabilities:** Process payments and send verification responses

---

## Central Process

### **Process 0: PetPal System**
**Description:** Complete pet marketplace and management platform that handles:
- User authentication and profile management
- Pet and breed information display
- Pet marketplace with listing fees and approvals
- Accessory e-commerce with cart and checkout
- Payment processing integration
- Wishlist management
- Buyer-seller communication
- Homepage content management

---

## Data Flows

### **Flows FROM External Entities TO System**

#### From Guest User → PetPal System:
1. **Browse Requests**
   - View breeds
   - View pet catalog (Browse Pets)
   - View accessories
   - View homepage content

#### From Registered Buyer → PetPal System:
2. **Registration Data**
   - First name, last name, email, phone, password

3. **Login Credentials**
   - Email and password

4. **Shopping Actions**
   - Add to cart
   - Update cart quantities
   - Checkout request with shipping details
   - Payment confirmation

5. **Wishlist Actions**
   - Add pet to wishlist
   - Remove from wishlist
   - View wishlist

6. **Communication**
   - Chat messages to sellers
   - Chat thread requests

7. **Search & Filter Criteria**
   - Breed filters (size, energy level, grooming, etc.)
   - Pet filters (breed, age, city, price range)
   - Accessory filters (category, price range)

8. **Profile Updates**
   - Phone number, user type changes

9. **Password Management**
   - Password reset requests
   - Password change requests

#### From Pet Seller → PetPal System:
10. **Listing Fee Payment**
    - Payment for 5 pet submissions (NPR 100)

11. **Pet Submission Data**
    - Breed, age, gender, price, description
    - Pet images (up to 3)
    - Location (city, state, address, coordinates)
    - Health information (vaccination, certificate)
    - Gender availability, weight, color

12. **My Pets Management**
    - View submitted pets
    - Check submission status

#### From System Administrator → PetPal System:
13. **Breed Management**
    - Create/update breed information
    - Upload breed images

14. **Pet Catalog Management**
    - Add admin-curated pets (Browse Pets)
    - Update pet information

15. **Accessory Management**
    - Add/update accessories
    - Manage stock levels
    - Set prices

16. **Pet Review Actions**
    - Approve user-submitted pets
    - Reject user-submitted pets
    - Add admin notes

17. **Homepage Configuration**
    - Create hero sections
    - Add feature cards
    - Manage testimonials
    - Update homepage settings

18. **System Configuration**
    - Update listing price (default NPR 100)

#### From eSewa Payment Gateway → PetPal System:
19. **Payment Verification Response**
    - Transaction status (success/failure)
    - Transaction details
    - Payment confirmation data

---

### **Flows FROM System TO External Entities**

#### From PetPal System → Guest User:
20. **Public Content**
    - Breed listings with details
    - Pet catalog (Browse Pets section)
    - Accessory catalog
    - Homepage with hero sections and features
    - Pet and breed details

#### From PetPal System → Registered Buyer:
21. **Authentication Responses**
    - Login success/failure
    - Registration confirmation
    - Password reset emails
    - Session status

22. **Shopping Information**
    - Cart contents and totals
    - Stock availability status
    - Product details

23. **Order Confirmations**
    - Order details and order ID
    - Payment success/failure status
    - Transaction receipts

24. **Wishlist Contents**
    - Saved pets (Browse & Marketplace)
    - Pet availability status

25. **Chat Messages**
    - Messages from sellers
    - Chat thread list
    - Unread message counts

26. **Profile Information**
    - User details
    - Order history

#### From PetPal System → Pet Seller:
27. **Listing Payment Confirmation**
    - Payment success/failure
    - Remaining submissions count (out of 5)

28. **Pet Submission Status**
    - Pending review notification
    - Approval confirmation
    - Rejection notification with admin notes

29. **My Pets Dashboard**
    - List of submitted pets with status
    - Pet details and submission date

30. **Chat Messages**
    - Messages from interested buyers
    - Chat notifications

#### From PetPal System → System Administrator:
31. **Admin Dashboard Data**
    - Pending pet reviews
    - System statistics
    - User management data

32. **Management Confirmations**
    - Update success messages
    - Configuration changes confirmed

#### From PetPal System → eSewa Payment Gateway:
33. **Payment Requests**
    - Transaction UUID
    - Amount details (listing fees or order totals)
    - Product information
    - Success/failure callback URLs
    - Digital signature for verification

---

## System Boundary

**Inside the System:**
- All database storage (User, Pet, Breed, Accessory, Cart, Order, Transaction, etc.)
- All business logic and processing
- Authentication and authorization
- Payment verification logic
- Stock management
- Chat message storage and routing

**Outside the System:**
- User interfaces (browsers, devices)
- eSewa payment gateway infrastructure
- Email delivery service (for password resets)

---

## Key Characteristics

### **System Inputs:**
- User credentials and registration data
- Pet listings with images and location
- Shopping cart operations
- Payment confirmations from eSewa
- Admin configurations
- Search and filter parameters
- Chat messages

### **System Outputs:**
- Content displays (breeds, pets, accessories)
- Shopping cart and order confirmations
- Payment status notifications
- Pet submission status updates
- Chat messages and notifications
- Admin dashboards

### **External Interactions:**
- **eSewa Payment Gateway:** Bidirectional payment processing
- **Email Service:** Password reset emails (implicit)
- **Map Services:** Location coordinates (implicit in pet submissions)

---

## Business Context

**Primary Functions:**
1. **Information Portal:** Comprehensive breed information and pet catalog
2. **E-Commerce Platform:** Accessory sales with cart and checkout
3. **Marketplace:** User-to-user pet sales with listing fees
4. **Communication Hub:** Chat between buyers and sellers
5. **Content Management:** Configurable homepage and content

**Revenue Streams:**
1. Listing fees from pet sellers (NPR 100 for 5 submissions)
2. Accessory sales
3. Potential transaction fees or commissions (future)

**User Roles:**
- **Guest:** Browse only
- **Buyer:** Browse + Purchase + Communicate
- **Seller:** Buyer features + List pets
- **Admin:** Full system control

---

## Data Flow Summary Table

| Flow # | From | To | Data Description |
|--------|------|-----|-----------------|
| 1 | Guest User | System | Browse requests (breeds, pets, accessories) |
| 2-9 | Registered Buyer | System | Registration, login, shopping, wishlist, chat |
| 10-12 | Pet Seller | System | Listing payment, pet submissions, management |
| 13-18 | Administrator | System | Content management, reviews, configuration |
| 19 | eSewa | System | Payment verification responses |
| 20 | System | Guest User | Public content display |
| 21-26 | System | Registered Buyer | Auth, shopping, orders, wishlist, chat |
| 27-30 | System | Pet Seller | Payment confirmations, submission status, chat |
| 31-32 | System | Administrator | Dashboard data, confirmations |
| 33 | System | eSewa | Payment requests with transaction details |

---

## System Constraints & Rules

1. **Authentication Required:**
   - Shopping cart operations
   - Wishlist management
   - Pet listing submissions
   - Chat communication
   - Checkout and payments

2. **Payment Required:**
   - Pet listing submission (NPR 100 for 5 submissions)
   - Accessory purchases

3. **Approval Required:**
   - User-submitted pets must be approved by admin before marketplace display

4. **Stock Management:**
   - Real-time stock validation
   - Atomic stock decrease after successful payment
   - Prevent overselling

5. **Multi-Submission Tracking:**
   - One payment = 5 pet submissions
   - Track usage count per payment

---

## Diagram Notation Guide

### **For Visual Representation:**

**External Entities:**
- Rectangle (or person icon)
- Label: Entity name

**Central Process:**
- Large circle (or rounded rectangle)
- Label: "0" and "PetPal System"

**Data Flows:**
- Arrows with labels
- Direction indicates data movement
- Label describes the data being transferred

**Example ASCII Representation:**
```
┌─────────────────┐
│   Guest User    │───(1: Browse Requests)──────┐
└─────────────────┘                              │
                                                 │
┌─────────────────┐                              │        ┌────────────────────┐
│ Registered      │───(2-9: Shopping/Auth)───────┤        │                    │
│ Buyer           │◄──(21-26: Content/Orders)────┤        │                    │
└─────────────────┘                              │        │                    │
                                                 ├───────►│   0. PetPal       │
┌─────────────────┐                              │        │      System        │
│  Pet Seller     │───(10-12: Listings)──────────┤        │                    │
│                 │◄──(27-30: Status/Chat)───────┤        │                    │
└─────────────────┘                              │        │                    │
                                                 │        └────────────────────┘
┌─────────────────┐                              │                  │  ▲
│ Administrator   │───(13-18: Management)────────┤                  │  │
│                 │◄──(31-32: Dashboard)─────────┘        (33)      │  │ (19)
└─────────────────┘                                        │        │  │
                                                           ▼        │  │
                                                    ┌──────────────────────┐
                                                    │  eSewa Payment       │
                                                    │  Gateway             │
                                                    └──────────────────────┘
```

---

## Next Steps

**For Level 1 DFD:** Decompose the central "PetPal System" into 8 major processes:
1. User Management
2. Pet Information Management
3. Pet Marketplace Management
4. Accessory Shopping
5. Order & Payment Processing
6. Wishlist Management
7. Communication System
8. Homepage Content Management

**For Level 2 DFD:** Further decompose each Level 1 process into detailed sub-processes showing validation, business logic, and state transitions.

---

**Recommended Tools for Visual Creation:**
- Draw.io / Diagrams.net (free, web-based)
- Lucidchart (professional)
- Microsoft Visio (enterprise)
- PlantUML (code-based, version controllable)
- Creately (collaborative)

**Color Coding Suggestions:**
- External Entities: Light blue
- PetPal System: Green
- Data Flows (Inputs): Orange arrows
- Data Flows (Outputs): Blue arrows
- Payment Gateway: Yellow (special external system)

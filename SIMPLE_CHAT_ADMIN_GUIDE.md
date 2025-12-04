# 💬 Simple Chat Admin - Quick Guide

## How to Access

1. Go to Django Admin: `/admin/`
2. Click on **"Chat messages"** in the sidebar
3. You'll see all chat messages from all conversations

## What You Can See

### Message List Page
- Conversation info (pet, buyer, seller)
- Who sent the message (Buyer/Seller)
- Message preview
- Read status (✓ or ✓✓)
- Timestamp

### Message Detail Page
When you click on any message, you'll see:

1. **Pet Information** - Breed, price, location, image
2. **Full Conversation** - All messages in order with colors:
   - Blue: Buyer messages
   - Purple: Seller messages
   - Yellow: Current message you clicked
3. **Admin Reply Form** - At the bottom

## How to Reply

1. Click on any message
2. Scroll to the bottom - you'll see "📤 Admin Reply" section
3. Select who you want to reply as:
   - 👤 **Buyer** - Reply as the buyer
   - 🏪 **Seller** - Reply as the seller
4. Type your message
5. Click "📤 Send Reply"
6. Page will reload with your new message

## That's It!

Simple, single-page chat management. No complex threads or separate sections - just messages with the ability to reply!

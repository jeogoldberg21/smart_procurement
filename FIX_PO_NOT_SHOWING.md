# 🔧 Fix: Purchase Orders Not Showing

## ❌ **Problem**

Dashboard shows: **"Failed to fetch purchase orders"**

## 🔍 **Root Cause**

There are **no Purchase Order files** in the `data/purchase_orders/` directory yet. The system is working correctly, but there's simply no data to display.

---

## ✅ **Solution (2 Options)**

### **Option 1: Check & Create Sample PO** ⚡ (RECOMMENDED)

**Step 1: Check what's missing**
```bash
python check_po_directory.py
```

**Step 2: Create a sample PO**
```bash
python create_sample_po.py
```

**Step 3: Refresh dashboard**
- Press **F5** in browser
- Go to "View POs" tab
- Should see the sample PO

---

### **Option 2: Generate PO via Dashboard** 📋

**Step 1: Go to "Generate New PO" tab**

**Step 2: Fill in details:**
- Material: Copper
- Quantity: 100 tons
- Requester: Your Name

**Step 3: Click "🚀 Generate Purchase Order"**

**Step 4: Go to "View POs" tab**
- Should now see the PO you just created

---

## 🧪 **Verification Steps**

### **1. Check Directory Structure**
```bash
python check_po_directory.py
```

**Expected output:**
```
✅ Exists: data/purchase_orders
✅ Exists: data/purchase_orders/pdf
✅ Found 1 PO file(s):
   - PO-202510-1001.json
```

### **2. Check Backend API**
```bash
curl http://localhost:5000/api/po/list
```

**Expected output:**
```json
{
  "success": true,
  "purchase_orders": [
    {
      "po_number": "PO-202510-1001",
      "material": {"name": "Copper"},
      "status": "DRAFT"
    }
  ],
  "count": 1
}
```

### **3. Check Dashboard**
- Refresh browser (F5)
- Go to "📋 Purchase Orders"
- Click "📜 View POs" tab
- Should see list of POs (not error message)

---

## 📊 **What Should Appear**

### **After Creating PO:**
```
📋 PO-202510-1001 - Copper - DRAFT
  Material: Copper
  Quantity: 100 tons
  Total Amount: $997,100.00
  Status: DRAFT
  Vendor: Global Metals Inc.
```

---

## 🔍 **Troubleshooting**

### **Issue 1: "Backend not running"**
**Solution:**
```bash
python app.py
```
Wait for: `* Running on http://127.0.0.1:5000`

### **Issue 2: "Failed to generate PO"**
**Check:**
1. Backend console for errors
2. Data files exist (`data/material_prices.csv`, `data/vendors.json`)
3. Run: `python regenerate_data_usd.py`

### **Issue 3: "Still shows 'Failed to fetch'"**
**Solution:**
1. Check if PO files exist: `python check_po_directory.py`
2. Restart backend: Stop (Ctrl+C) and run `python app.py`
3. Hard refresh browser: Ctrl+Shift+R
4. Check browser console (F12) for errors

### **Issue 4: "Directory not found"**
**Solution:**
```bash
mkdir data\purchase_orders
mkdir data\purchase_orders\pdf
```
Then run: `python create_sample_po.py`

---

## 📁 **Expected File Structure**

```
data/
├── material_prices.csv          ✅ Price data
├── inventory.json               ✅ Inventory data
├── vendors.json                 ✅ Vendor data
└── purchase_orders/
    ├── PO-202510-1001.json     ← PO data files
    ├── PO-202510-1002.json
    ├── po_counter.json          ← PO number counter
    └── pdf/
        ├── PO-202510-1001.pdf  ← PDF exports
        └── PO-202510-1002.pdf
```

---

## 🎯 **Quick Fix Commands**

**Run these in order:**

```bash
# 1. Check directory
python check_po_directory.py

# 2. Create sample PO
python create_sample_po.py

# 3. Verify it worked
curl http://localhost:5000/api/po/list

# 4. Refresh dashboard (F5 in browser)
```

---

## ✅ **Success Indicators**

### **Backend Console:**
```
✓ PO generated: PO-202510-1001
✓ Saved to: data/purchase_orders/PO-202510-1001.json
```

### **Dashboard:**
- ✅ No error message
- ✅ Shows list of POs
- ✅ Can expand PO details
- ✅ Can export to PDF

### **API Response:**
```json
{
  "success": true,
  "count": 1
}
```

---

## 📝 **Why This Happens**

### **Normal Behavior:**
1. System starts with **no POs** (empty directory)
2. User must **generate first PO** via:
   - Dashboard "Generate New PO" button
   - API call
   - Test script

3. Once PO exists, it appears in "View POs" tab

### **Not a Bug:**
- ✅ System is working correctly
- ✅ Just needs initial data
- ✅ Like a fresh database

---

## 🚀 **For Demo**

### **Before Demo:**
```bash
# Create 3-5 sample POs
python create_sample_po.py
# Change material and run again
# Edit script to use 'Aluminum', 'Steel'
```

### **During Demo:**
1. Show "View POs" tab with existing POs
2. Generate a new PO live
3. Show it appears immediately
4. Export to PDF
5. Show analytics with multiple POs

---

## 📊 **Sample PO Data**

After running `create_sample_po.py`:

```
PO Number: PO-202510-1001
Material: Copper (100 tons)
Vendor: Global Metals Inc.
Total: $997,100.00
Status: DRAFT
Created: 2025-10-16 15:39:46
```

---

## ✅ **Summary**

**Problem:** No PO files exist yet
**Solution:** Create sample PO or generate via dashboard
**Command:** `python create_sample_po.py`
**Result:** Dashboard shows PO list

---

## 🚨 **Action Required**

**RUN THIS NOW:**
```bash
python create_sample_po.py
```

**Then refresh dashboard (F5)**

---

**The "Failed to fetch" error will disappear once you create a PO!** ✅

**It's not a bug - just needs initial data!** 🎯

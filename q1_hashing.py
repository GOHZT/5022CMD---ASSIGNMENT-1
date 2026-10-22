"""
5022CMD Advanced Algorithms - Question 1 (UPGRADED)
Hash Table with Open Addressing (Linear Probing)
Pharmacy Inventory System: Insert, Search, Edit, Delete, Display, Experiment
"""

import time


# ============================================================
# ENTITY CLASS
# ============================================================
class PharmacyProduct:
    """
    Entity class representing a pharmacy product (medicine).
    Attributes:
        product_id (int): Unique identifier.
        name (str): Medicine name.
        price (float): Price in RM.
        stock (int): Quantity in stock.
    """
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return (f"ID: {self.product_id:<6} | Name: {self.name:<25} | "
                f"Price: RM{self.price:>7.2f} | Stock: {self.stock:>4}")


# ============================================================
# HASH TABLE (Open Addressing + Linear Probing)
# ============================================================
class HashTable:
    """
    Hash Table using Open Addressing with Linear Probing.
    Supports insert, search, delete, and display.
    """
    EMPTY = None
    DELETED = object()  # Sentinel for deleted slots

    def __init__(self, capacity=11):
        self.capacity = capacity
        self.size = 0
        self.slots = [self.EMPTY] * capacity
        self.keys = [None] * capacity

    def _hash(self, key):
        """Division method hash function."""
        return key % self.capacity

    def _probe(self, key):
        """
        Linear probing: find slot for key.
        Returns (index, found) where found indicates if key exists.
        """
        index = self._hash(key)
        start_index = index
        while self.slots[index] is not self.EMPTY:
            if self.slots[index] is not self.DELETED and self.keys[index] == key:
                return index, True
            index = (index + 1) % self.capacity
            if index == start_index:
                break
        return index, False

    def insert(self, key, value):
        """Insert a key-value pair. Returns the slot index used."""
        if self.size >= self.capacity // 2:
            self._resize()
        index, found = self._probe(key)
        if found:
            self.slots[index] = value  # update existing
            return index, False  # not a new insert
        self.slots[index] = value
        self.keys[index] = key
        self.size += 1
        return index, True  # new insert

    def search(self, key):
        """Search for a key. Returns value or None."""
        index, found = self._probe(key)
        if found:
            return self.slots[index]
        return None

    def delete(self, key):
        """Delete a key (mark slot as DELETED). Returns True if deleted."""
        index, found = self._probe(key)
        if found:
            self.slots[index] = self.DELETED
            self.keys[index] = None
            self.size -= 1
            return True
        return False

    def update(self, key, new_name=None, new_price=None, new_stock=None):
        """
        Edit an existing product's fields.
        Returns (success, product) where product is the updated object.
        """
        product = self.search(key)
        if product is None:
            return False, None
        if new_name is not None and new_name.strip() != "":
            product.name = new_name
        if new_price is not None:
            product.price = new_price
        if new_stock is not None:
            product.stock = new_stock
        return True, product

    def _resize(self):
        """Double capacity and rehash all elements."""
        old_slots = self.slots
        old_keys = self.keys
        self.capacity *= 2
        self.slots = [self.EMPTY] * self.capacity
        self.keys = [None] * self.capacity
        self.size = 0
        for i in range(len(old_slots)):
            if old_slots[i] is not self.EMPTY and old_slots[i] is not self.DELETED:
                self.insert(old_keys[i], old_slots[i])

    def display(self):
        """Display all occupied slots in a clean table."""
        print("\n" + "=" * 80)
        print(f"{'Slot':<6} | {'Product ID':<10} | {'Name':<25} | {'Price':<10} | {'Stock':<6}")
        print("-" * 80)
        found = False
        for i in range(self.capacity):
            if self.slots[i] is not self.EMPTY and self.slots[i] is not self.DELETED:
                p = self.slots[i]
                print(f"{i:<6} | {p.product_id:<10} | {p.name:<25} | "
                      f"RM{p.price:<7.2f} | {p.stock:<6}")
                found = True
        if not found:
            print("(No products in inventory)")
        print("=" * 80)
        print(f"Total products: {self.size} | Table capacity: {self.capacity} | "
              f"Load factor: {self.size/self.capacity:.2f}")

    def get_all_products(self):
        """Return a list of all products (for array comparison)."""
        products = []
        for i in range(self.capacity):
            if self.slots[i] is not self.EMPTY and self.slots[i] is not self.DELETED:
                products.append(self.slots[i])
        return products


# ============================================================
# ARRAY (for comparison)
# ============================================================
class ProductArray:
    """One-dimensional array for storing products."""
    def __init__(self):
        self.data = []

    def insert(self, product):
        self.data.append(product)

    def search(self, product_id):
        """Linear search."""
        for p in self.data:
            if p.product_id == product_id:
                return p
        return None

    def delete(self, product_id):
        for i, p in enumerate(self.data):
            if p.product_id == product_id:
                del self.data[i]
                return True
        return False


# ============================================================
# VALIDATION HELPERS
# ============================================================
def get_int(prompt, min_value=None, max_value=None):
    """Prompt until a valid integer is entered."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"  ⚠ Value must be at least {min_value}. Try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"  ⚠ Value must be at most {max_value}. Try again.")
                continue
            return value
        except ValueError:
            print("  ⚠ Invalid input. Please enter a whole number.")


def get_float(prompt, min_value=0.0):
    """Prompt until a valid float is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value < min_value:
                print(f"  ⚠ Value must be at least {min_value}. Try again.")
                continue
            return value
        except ValueError:
            print("  ⚠ Invalid input. Please enter a number (e.g., 5.90).")


def get_nonempty_string(prompt):
    """Prompt until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ⚠ Input cannot be empty. Try again.")


def confirm(prompt):
    """Ask for yes/no confirmation."""
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print("  ⚠ Please enter 'y' or 'n'.")


# ============================================================
# EXPERIMENT: Hash Table vs Array
# ============================================================
def run_experiment(hash_table, array, search_id=1042, iterations=10000, rounds=10):
    """Compare search performance of hash table vs array."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON: Hash Table vs Array")
    print(f"Searching for Product ID {search_id}")
    print(f"{iterations} iterations x {rounds} rounds")
    print("=" * 60)

    hash_times = []
    array_times = []

    for r in range(1, rounds + 1):
        # Hash table search
        start = time.perf_counter_ns()
        for _ in range(iterations):
            hash_table.search(search_id)
        end = time.perf_counter_ns()
        h_time = end - start
        hash_times.append(h_time)

        # Array search
        start = time.perf_counter_ns()
        for _ in range(iterations):
            array.search(search_id)
        end = time.perf_counter_ns()
        a_time = end - start
        array_times.append(a_time)

        print(f"Round {r:>2}: Hash Table = {h_time:>12,} ns | "
              f"Array = {a_time:>12,} ns")

    avg_hash = sum(hash_times) / len(hash_times)
    avg_array = sum(array_times) / len(array_times)

    print("-" * 60)
    print(f"Average Hash Table: {avg_hash:>15,.0f} ns")
    print(f"Average Array:      {avg_array:>15,.0f} ns")
    print(f"Hash Table is approximately {avg_array/avg_hash:.2f}x faster than Array.")
    print("=" * 60)


# ============================================================
# CLI FUNCTIONS
# ============================================================
def do_insert(pharmacy, product_array):
    """Insert a new product."""
    print("\n--- INSERT NEW PRODUCT ---")
    pid = get_int("Enter Product ID (positive integer): ", min_value=1)

    # Check for duplicate
    if pharmacy.search(pid) is not None:
        print(f"  ⚠ Product ID {pid} already exists!")
        if not confirm("Do you want to update the existing product instead?"):
            return
        # Fall through to edit
        do_edit(pharmacy)
        return

    name = get_nonempty_string("Enter Product Name: ")
    price = get_float("Enter Price (RM): ", min_value=0.0)
    stock = get_int("Enter Stock Quantity: ", min_value=0)

    product = PharmacyProduct(pid, name, price, stock)
    slot, is_new = pharmacy.insert(pid, product)
    product_array.insert(product)

    if is_new:
        print(f"\n✓ Product inserted successfully into slot [{slot}]")
    else:
        print(f"\n✓ Product updated at slot [{slot}]")


def do_search(pharmacy):
    """Search for a product."""
    print("\n--- SEARCH PRODUCT ---")
    pid = get_int("Enter Product ID to search: ", min_value=1)

    start = time.perf_counter_ns()
    product = pharmacy.search(pid)
    end = time.perf_counter_ns()

    if product:
        print("\n✓ Product Found!")
        print(f"  {product}")
        print(f"  Search completed in {end - start:,} nanoseconds (Hash Table)")
    else:
        print(f"\n✗ Product with ID {pid} not found.")


def do_edit(pharmacy):
    """Edit an existing product."""
    print("\n--- EDIT PRODUCT ---")
    pid = get_int("Enter Product ID to edit: ", min_value=1)

    product = pharmacy.search(pid)
    if not product:
        print(f"  ✗ Product with ID {pid} not found.")
        return

    print(f"\nCurrent details:\n  {product}")
    print("\nLeave blank to keep current value.")

    new_name = input(f"New Name [{product.name}]: ").strip()
    new_price_str = input(f"New Price [{product.price:.2f}]: ").strip()
    new_stock_str = input(f"New Stock [{product.stock}]: ").strip()

    new_name = new_name if new_name else None
    try:
        new_price = float(new_price_str) if new_price_str else None
    except ValueError:
        print("  ⚠ Invalid price. Keeping current value.")
        new_price = None
    try:
        new_stock = int(new_stock_str) if new_stock_str else None
    except ValueError:
        print("  ⚠ Invalid stock. Keeping current value.")
        new_stock = None

    success, updated = pharmacy.update(pid, new_name, new_price, new_stock)
    if success:
        print(f"\n✓ Product updated successfully!")
        print(f"  {updated}")


def do_delete(pharmacy, product_array):
    """Delete a product."""
    print("\n--- DELETE PRODUCT ---")
    pid = get_int("Enter Product ID to delete: ", min_value=1)

    product = pharmacy.search(pid)
    if not product:
        print(f"  ✗ Product with ID {pid} not found.")
        return

    print(f"\nProduct to delete:\n  {product}")
    if not confirm("Are you sure you want to delete this product?"):
        print("  Deletion cancelled.")
        return

    if pharmacy.delete(pid):
        product_array.delete(pid)
        print(f"\n✓ Product with ID {pid} deleted successfully.")
    else:
        print(f"  ✗ Failed to delete product.")


# ============================================================
# MAIN MENU
# ============================================================
def main():
    pharmacy = HashTable(capacity=11)
    product_array = ProductArray()

    # Pre-defined records
    pre_defined = [
        PharmacyProduct(1042, "Paracetamol 500mg", 5.90, 120),
        PharmacyProduct(2043, "Amoxicillin 250mg", 12.50, 80),
        PharmacyProduct(3054, "Ibuprofen 400mg", 7.20, 200),
        PharmacyProduct(4065, "Cetirizine 10mg", 4.80, 150),
        PharmacyProduct(5076, "Omeprazole 20mg", 15.30, 60),
    ]
    for product in pre_defined:
        pharmacy.insert(product.product_id, product)
        product_array.insert(product)

    print("=" * 60)
    print("  WELCOME TO PHARMACY INVENTORY SYSTEM")
    print("  (Hash Table with Open Addressing - Linear Probing)")
    print("=" * 60)
    print(f"  {len(pre_defined)} pre-defined products loaded.")
    print("=" * 60)

    while True:
        print("\n┌─────────────────────────────────────┐")
        print("│         MAIN MENU                   │")
        print("├─────────────────────────────────────┤")
        print("│  1. Insert Product                  │")
        print("│  2. Search Product                  │")
        print("│  3. Edit Product                    │")
        print("│  4. Delete Product                  │")
        print("│  5. Display All Products            │")
        print("│  6. Run Performance Experiment      │")
        print("│  7. Exit                            │")
        print("└─────────────────────────────────────┘")

        choice = input("Enter choice (1-7): ").strip()

        if choice == '1':
            do_insert(pharmacy, product_array)
        elif choice == '2':
            do_search(pharmacy)
        elif choice == '3':
            do_edit(pharmacy)
        elif choice == '4':
            do_delete(pharmacy, product_array)
        elif choice == '5':
            pharmacy.display()
        elif choice == '6':
            run_experiment(pharmacy, product_array)
        elif choice == '7':
            print("\nThank you for using Pharmacy Inventory System. Goodbye!")
            break
        else:
            print("  ⚠ Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
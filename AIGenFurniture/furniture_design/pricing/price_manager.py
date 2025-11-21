# furniture_design/pricing/price_manager.py
import csv
from functools import lru_cache
from pathlib import Path


class PriceNotFoundError(ValueError):
    pass


class PriceManager:
    PRICE_FILE = Path(__file__).parent / "price_list.csv"

    @classmethod
    @lru_cache(maxsize=1)
    def load_prices(cls):
        prices = {}
        with open(cls.PRICE_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (
                    row["type"].strip().lower(),
                    row["material"].strip().lower()
                )
                prices[key] = {
                    "price": float(row["price"]),
                    "currency": row["currency"],
                    "unit": row["unit"].strip(),
                    "minimum_order": float(row["minimum_order"])
                }
        return prices

    @classmethod
    def clear_cache(cls):
        cls.load_prices.cache_clear()

    @classmethod
    def get_price_for_item(cls, item_type, material):
        key = (item_type.lower(), material.lower())
        prices = cls.load_prices()
        if key not in prices:
            raise PriceNotFoundError(
                f"Price not found for type '{item_type}', material '{material}'"
            )
        return prices[key]["price"]

    @classmethod
    def get_unit_for_item(cls, item_type, material):
        key = (item_type.lower(), material.lower())
        prices = cls.load_prices()
        if key not in prices:
            raise PriceNotFoundError(
                f"Unit not found for type '{item_type}', material '{material}'"
            )
        return prices[key]["unit"]

    @classmethod
    def get_min_qty_for_item(cls, item_type, material):
        key = (item_type.lower(), material.lower())
        prices = cls.load_prices()
        if key not in prices:
            raise PriceNotFoundError(
                f"Unit not found for type '{item_type}', material '{material}'"
            )
        return prices[key]["minimum_order"]

# ===========================================================
#                SIMPLE BUILT-IN TEST SUITE
# ===========================================================

def _run_basic_tests():
    import tempfile

    print("Running inline PriceManager tests...\n")

    # Create a temporary CSV for testing
    csv_data = """type,material,price,unit
board,white,100.5,m2
board,oak,150,m2
accessory,handle,5,pcs
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        test_csv = Path(tmpdir) / "price_list.csv"
        test_csv.write_text(csv_data, encoding="utf-8")

        # Point PriceManager to test CSV
        PriceManager.PRICE_FILE = test_csv
        PriceManager.clear_cache()

        # Start tests
        try:
            print("✔ Testing valid price lookup...")
            assert PriceManager.get_price_for_item("board", "white") == 100.5
            assert PriceManager.get_price_for_item("BOARD", "OAK") == 150
            assert PriceManager.get_price_for_item("accessory", "handle") == 5

            print("✔ Testing unit lookup...")
            assert PriceManager.get_unit_for_item("board", "white") == "m2"
            assert PriceManager.get_unit_for_item("accessory", "handle") == "pcs"

            print("✔ Testing missing price error...")
            try:
                PriceManager.get_price_for_item("board", "black")
                raise Exception("Expected PriceNotFoundError not raised")
            except PriceNotFoundError:
                pass

            print("✔ Testing cache behaviour...")
            PriceManager.clear_cache()
            PriceManager.load_prices()
            initial_hits = PriceManager.load_prices.cache_info().hits
            PriceManager.get_price_for_item("board", "white")
            later_hits = PriceManager.load_prices.cache_info().hits
            assert later_hits > initial_hits

            print("\nAll tests passed successfully! 🎉")

        except AssertionError as e:
            print("\n❌ TEST FAILED")
            print(e)
            raise


# ===========================================================
#                RUN TESTS IF EXECUTED DIRECTLY
# ===========================================================
if __name__ == "__main__":
    # _run_basic_tests()
    print(PriceManager.load_prices())

    print(PriceManager.get_price_for_item('pal', 'Gri Onix U960 ST9'))
    print(PriceManager.get_unit_for_item('pal', 'Gri Onix U960 ST9'))
    print(PriceManager.get_min_qty_for_item('pal', 'Gri Onix U960 ST9'))
    print(PriceManager.get_price_for_item('cant', '0.4'))


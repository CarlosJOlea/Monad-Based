import pytest
from validate.date_validator import validate_date
from validate.price_validator import validate_price
from validate.product_validator import validate_product
from validate.quantity_validator import validate_quantity
from validate.customer_validator import validate_customer

def test_validate_date_ok():
    v = validate_date("2025-09-01")
    assert v.is_success()
    assert v.get_value() == "2025-09-01"

def test_validate_date_empty():
    v = validate_date("")
    assert v.is_failure()

def test_validate_price_ok():
    v = validate_price("100.5")
    assert v.is_success()
    assert v.get_value() == 100.5

def test_validate_price_negative():
    v = validate_price("-5")
    assert v.is_failure()

def test_validate_product_ok():
    v = validate_product("Widget A")
    assert v.is_success()

def test_validate_product_empty():
    v = validate_product(" ")
    assert v.is_failure()

def test_validate_quantity_ok():
    v = validate_quantity("10")
    assert v.is_success()
    assert v.get_value() == 10

def test_validate_quantity_invalid():
    v = validate_quantity("abc")
    assert v.is_failure()

def test_validate_customer_ok():
    v = validate_customer("Cliente X")
    assert v.is_success()

def test_validate_customer_empty():
    v = validate_customer(" ")
    assert v.is_failure()

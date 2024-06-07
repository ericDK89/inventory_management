"""File to handle integrations tests"""

from fastapi import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product_schema import ProductCreate
from app.models.product import Product


def test_create_product(client: TestClient, db_session: Session) -> None:
    """Def to test creation product"""
    create_response: Response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 9.99,
            "stock_quantity": 10,
        },
    )

    # * Assert the creation product response
    assert create_response.status_code == 201
    assert create_response.json() == {"success": "Product successfully created"}

    db_product: Product = (
        db_session.query(Product).filter(Product.name == "Test Product").first()
    )

    # * Make sure that the db is working
    assert db_product is not None
    assert db_product.name == "Test Product"
    assert db_product.description == "Test Description"
    assert db_product.price == 9.99
    assert db_product.stock_quantity == 10


def test_get_all_products(client: TestClient, db_session: Session) -> None:
    """Def to integration test for get all products"""
    product_data_one = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=9.99,
        stock_quantity=10,
    )

    product_data_two = ProductCreate(
        name="Test Product two",
        description="Test Description two",
        price=9.99,
        stock_quantity=10,
    )

    all_products: List[Product] = [
        Product(**product_data_one.model_dump()),
        Product(**product_data_two.model_dump()),
    ]

    db_session.add_all(all_products)
    db_session.commit()

    get_products: Response = client.get("/products")

    assert get_products.status_code == 200
    assert get_products.json() == {
        "success": [
            {
                "name": "Test Product",
                "description": "Test Description",
                "price": 9.99,
                "stock_quantity": 10,
                "id": 1,
            },
            {
                "name": "Test Product two",
                "description": "Test Description two",
                "price": 9.99,
                "stock_quantity": 10,
                "id": 2,
            },
        ]
    }


def test_get_product_by_id(client: TestClient, db_session: Session) -> None:
    """Def to integration test for get all products"""
    product_data_one = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=9.99,
        stock_quantity=10,
    )

    product_id = 1
    product: Product = Product(id=product_id, **product_data_one.model_dump())

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    get_product: Response = client.get(f"/product/{product_id}")

    assert get_product.status_code == 200
    assert get_product.json() == {
        "success": {
            "name": "Test Product",
            "description": "Test Description",
            "price": 9.99,
            "stock_quantity": 10,
            "id": 1,
        }
    }

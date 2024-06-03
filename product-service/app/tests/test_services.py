"""File to test all product_service methods"""

import pytest
from unittest.mock import MagicMock
from ..services.product_service import ProductService
from ..schemas.product_schema import ProductCreate
from ..models.product import Product


@pytest.fixture(scope="function")
def product_repository_mock() -> MagicMock:
    """Def to create the MagicMock to be used on all the code"""
    return MagicMock()


@pytest.fixture(scope="function")
def product_service(product_repository_mock: MagicMock) -> ProductService:
    """Def to generate product_service to be used on all the code"""
    return ProductService(product_repository_mock)


def test_create_product_when_product_already_exists(
    product_service: ProductService, product_repository_mock: MagicMock
) -> None:
    """Def to test if it's possible to create a product with a name that already exists

    Args:
        product_service (ProductService): Product Service
        product_repository_mock (MagicMock): Magic Mock
    """

    # * Define the product data of type ProductCreate
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=9.99,
        stock_quantity=10,
    )

    # * Create an instance of Product to simulate an existing product in the database
    existing_product = Product(id=1, **product_data.model_dump())

    # * Mock the repository to return the existing_product when findByName is called
    product_repository_mock.findByName.return_value = existing_product

    # * Attempt to create a product with the same data
    result = product_service.create(product_data)

    # * Assert that the result is the same as the existing product
    assert result == existing_product

    # * Ensure that the create method was not called
    product_repository_mock.create.assert_not_called()


def test_create_product_when_product_dont_exists(
    product_service: ProductService, product_repository_mock: MagicMock
) -> None:
    # TODO -> Add DocString

    # * Define the product data of type ProductCreate
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=9.99,
        stock_quantity=10,
    )

    # * Convert the ProductCreate instance to a Product instance
    new_product = Product(**product_data.model_dump())

    # * Mock the repository to return None when findByName is called, indicating that the product does not exist
    product_repository_mock.findByName.return_value = None

    # * Mock the repository to return the new product when create is called
    product_repository_mock.create.return_value = new_product

    # * Call the create method of the service
    result: Product = product_service.create(product_data)

    # * Assert that the repository's findByName method was called once with the product name and didn't find anything
    product_repository_mock.findByName.assert_called_once_with(product_data.name)

    # * Assert that the repository's create method was called once
    product_repository_mock.create.assert_called_once()

    # * Assert that the result is the new product
    assert result == new_product

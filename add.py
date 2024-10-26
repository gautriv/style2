from flask import Blueprint, render_template, request, current_app, flash
from sqlalchemy import or_
import permissions
import logging

logger = logging.getLogger(__name__)

@view_routes.route('/opl/search-to-view-products', methods=['GET', 'POST'])
def view_products():
    # Initialize variables
    form = SearchForm()
    products = []
    products_with_portfolios = []
    selected_product = None  # Initialize to avoid UnboundLocalError

    session = current_app.config['Session']()
    try:
        # Define the base query
        products_query = session.query(
            Product.product_id.label('product_id'),
            Product.product_name.label('product_name'),
            Product.product_status.label('product_status'),
            Product.last_updated.label('last_updated'),
            ProductPortfolios.category_name.label('category_name'),
            ProductType.product_type.label('product_type'),
            Product.is_admin_only.label('is_admin_only')  # Include and label
        ).outerjoin(ProductPortfolioMap, Product.product_id == ProductPortfolioMap.product_id)\
         .outerjoin(ProductPortfolios, ProductPortfolioMap.category_id == ProductPortfolios.category_id)\
         .join(ProductTypeMap, ProductTypeMap.product_id == Product.product_id)\
         .join(ProductType, ProductType.type_id == ProductTypeMap.type_id)\
         .outerjoin(ProductAlias, ProductAlias.product_id == Product.product_id)\
         .order_by(Product.product_name)

        # Check user permissions
        user_is_admin = permissions.opl_editor_permission.can()
        logger.debug(f"user_is_admin: {user_is_admin}")

        if not user_is_admin:
            products_query = products_query.filter(
                or_(
                    Product.is_admin_only == False,
                    Product.is_admin_only.is_(None)
                )
            )

        # Handle search parameters
        # ... existing code to handle search parameters ...

        # Fetch products
        products = products_query.all()

        # Process results
        product_dict = {}
        for product in products:
            product_id = product.product_id
            if product_id not in product_dict:
                product_dict[product_id] = {
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'product_status': product.product_status,
                    'last_updated': product.last_updated,
                    'portfolio_names': set(),
                    'product_types': set(),
                    'is_admin_only': product.is_admin_only  # Access using label
                }
            if product.category_name:
                product_dict[product_id]['portfolio_names'].add(product.category_name)
            if product.product_type:
                product_dict[product_id]['product_types'].add(product.product_type)

        # Convert to list
        products_with_portfolios = [
            {
                'product_id': prod['product_id'],
                'product_name': prod['product_name'],
                'product_status': prod['product_status'],
                'last_updated': prod['last_updated'],
                'portfolio_names': sorted(prod['portfolio_names']),
                'product_types': sorted(prod['product_types']),
                'is_admin_only': prod['is_admin_only']
            }
            for prod in product_dict.values()
        ]

    except Exception as e:
        logger.error(f"Error during product retrieval: {e}")
        flash('An error occurred while retrieving products.', 'error')
    finally:
        session.close()

    # Render template
    return render_template(
        'opl/view_search.html',
        form=form,
        products_with_portfolios=products_with_portfolios,
        user_is_admin=user_is_admin
    )

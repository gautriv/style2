<div class="pf-v5-c-form__group">
        <div class="pf-v5-c-check">
            <input class="pf-v5-c-check__input" type="checkbox" id="is_admin_only" name="is_admin_only" value="true">
            <label class="pf-v5-c-check__label" for="is_admin_only">Visible to Admins Only</label>
        </div>
    </div>



    <div class="pf-v5-c-form__group">
        <div class="pf-v5-c-check">
            <input class="pf-v5-c-check__input" type="checkbox" id="is_admin_only" name="is_admin_only" value="true" {% if product.is_admin_only %}checked{% endif %}>
            <label class="pf-v5-c-check__label" for="is_admin_only">Visible to Admins Only</label>
        </div>
    </div>



    is_admin_only = request.form.get('is_admin_only') == 'true'

        new_product = Product(
            # ... other fields ...
            is_admin_only=is_admin_only,
        )



        product.is_admin_only = request.form.get('is_admin_only') == 'true'



# Check if the user is an admin
        user_is_admin = 'admin' in current_user.roles

        if not user_is_admin:
            query = query.filter(Product.is_admin_only == False)


# Check if the user has admin permission
        user_is_admin = permissions.opl_admin_permission.can()

        if not user_is_admin:
            query = query.filter(Product.is_admin_only == False)



  # Check if the user has admin permission
        user_is_admin = permissions.opl_admin_permission.can()

        if not user_is_admin:
            query = query.filter(Product.is_admin_only == False)



  
        if not user_is_admin:
            query = query.filter(Product.is_admin_only == False)



            

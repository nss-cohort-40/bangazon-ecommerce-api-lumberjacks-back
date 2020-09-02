UPDATE ecommerceapi_order
  SET payment_type_id = NULL
  WHERE id=6;

DELETE from ecommerceapi_order
WHERE id = 9;
# Shopping cart validation using natural block body
context {
    action
    --begin
    Cart validation process:
    {{ if
    --begin
    Checking cart state:
    {{ action [Cart status checked] }}
    --end
    then { action [Cart is valid] }
    else { action [Cart requires attention] } }}
    --end
}

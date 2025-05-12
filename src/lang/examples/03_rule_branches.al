# Discount calculation rule demonstrating block structures
rule sales.pricing.discount {
    when
    --begin
    Evaluating premium status:
    {{ action
    --begin
    Checking membership details:
    - Status active
    - Premium tier
    --end }}
    --end
    then {
        action [Applying premium discount]
    }
    action
    --begin
    Processing standard pricing:
    {{ action [Using base rate calculation] }}
    --end
}

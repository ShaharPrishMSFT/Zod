# This example demonstrates block parsing limitations
# and documents current supported syntax

# Current supported forms:
function example.supported
{
    # 1. Inline natural blocks
    action [Simple inline action]
    input [Simple inline input]

    # 2. Natural blocks with --begin/--end
    action
        --begin
        Complex action with multiple lines
        and embedded formal expressions:
        {{ input [User input here] }}
        --end

    # 3. Simple if-then with inline blocks
    if [condition] then
    {
        action [then action]
    }
}

# Note: Current workaround is to use natural blocks
function example.workaround
{
    # Instead of nested braces, use natural blocks
    action
        --begin
        Complex logic here:
        {{ input [First input] }}
        {{ if [Some condition] then { action [Do something] } }}
        --end
}

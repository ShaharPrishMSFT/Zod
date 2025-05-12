# Age verification rule showing natural blocks and else clause
rule auth.verify
{
    if
    --begin
    Verifying user age:
    {{ input [Provide your age] }}
    --end
    then
    {
        action [Access granted for verified user]
    }
    else
    {
        action
        --begin
        Tell the user they must provide the age - they may not want to.
        --end
    }
}

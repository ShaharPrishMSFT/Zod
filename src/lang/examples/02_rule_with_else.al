# Age verification rule showing natural blocks and else clause
rule auth.verify {
    if
    --begin
    Verifying user age:
    {{ input [Age provided: {{ userAge }}] }}
    --end
    then {
        action [Access granted for verified user]
    }
    else {
        action
        --begin
        Access denied:
        {{ action [Age verification failed] }}
        --end
    }
}

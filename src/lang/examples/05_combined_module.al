# User session management module
# Demonstrates various block types and nesting
context auth.session.manager {
    action
    --begin
    Session initialization:
    {{ action [Creating new session] }}
    --end
}

# User verification function
function auth.user.verify {
    input userId
    if
    --begin
    Verifying credentials:
    {{ input [User ID: {{ userId }}] }}
    --end
    then {
        action [Credentials verified]
    }
    else
    --begin
    Verification failed:
    {{ action [Recording failure details] }}
    --end
}

# User greeting rules with nested blocks
rule {
    when
    --begin
    User authentication:
    {{ if
    --begin
    Checking login history:
    {{ action [History retrieved] }}
    --end
    then { action [User recognized] }
    else { action [New user detected] } }}
    --end
    then {
        action
        --begin
        Processing greeting:
        {{ action [Customizing welcome message] }}
        --end
    }
}

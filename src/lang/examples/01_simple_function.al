# Functions must have an ID
function uigreetingwelcome {
    input [userName]
    action
    --begin
    Processing greeting:
    {{ action
        --begin
        User details to include:
        - Name: {{ userName }}
        - Time: {{ currentTime }}
        --end
    }}
    --end
}

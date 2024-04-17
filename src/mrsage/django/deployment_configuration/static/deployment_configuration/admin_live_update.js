document.addEventListener(
    'DOMContentLoaded',
    event => {
        const raw_value_field = document.querySelector("[name=raw_value]");
        const option_type_field = document.querySelector("[name=option_type]")
        const option_type = option_type_field.options[option_type_field.selectedIndex].text;
        update_field_type(raw_value_field, option_type);
    }
)


document.addEventListener(
    'change',
    event => {
        if (event.target.name !== "option_type") return

        const raw_value_field = document.querySelector("[name=raw_value]");
        const option_type = event.target.options[event.target.selectedIndex].text;
        update_field_type(raw_value_field, option_type);
    }
)


const update_field_type = (raw_value_field, option_type) => {
    switch (option_type) {
        case "builtins.bool":
            raw_value_field.type = 'checkbox';
            raw_value_field.checked = !!raw_value_field.value;
            raw_value_field.value = raw_value_field.checked ? "True" : "False";
            break
        case "builtins.int":
            raw_value_field.type = 'number';
            break
        case "builtins.float":
            raw_value_field.type = 'number';
            break
        case "datetime.date":
            raw_value_field.type = 'date';
            break
        case "datetime.datetime":
            raw_value_field.type = 'datetime-local';
            break
        case "datetime.time":
            raw_value_field.type = 'time';
            break
        case "decimal.Decimal":
            raw_value_field.type = 'number';
            break

        // TODO Maybe there is an easy way to do iterables?

        default:
            raw_value_field.type = 'text'
    }
}

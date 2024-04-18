document.addEventListener(
    'DOMContentLoaded',
    event => {
        onload_update_field();
    }
)

window.addEventListener(
    'load',
    event => {
        setTimeout(onload_expand_start_open_fieldsets, 0);
    }
)


// Example of Buttons toggling several .test classNames
document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", () => ELS_test.forEach(el => el.classList.toggle(btn.dataset.class)));
});


document.addEventListener(
    'change',
    event => {
        if (event.target.name !== "option_type") return

        const raw_value_field = document.querySelector("[name=raw_value]");
        const option_type = event.target.options[event.target.selectedIndex].text;
        update_field_type(raw_value_field, option_type);
    }
)


const onload_expand_start_open_fieldsets = () => {
    const els = document.querySelectorAll('.collapsed.start-open');
    els.forEach(
        el => {
            el.classList.remove('collapsed');
            el.querySelector('.collapse-toggle').textContent = gettext('Hide');
        }
    );

}


const onload_update_field = () => {
    const raw_value_field = document.querySelector("[name=raw_value]");
    const option_type_field = document.querySelector("[name=option_type]")
    const option_type = option_type_field.options[option_type_field.selectedIndex].text;

    console.log(raw_value_field.value)
    update_field_type(raw_value_field, option_type);
}


const update_field_type = (raw_value_field, option_type) => {
    // This fixes a weird bug where a checkbox will inherit the value "on" for some reason
    const raw_value = raw_value_field.value;

    switch (option_type) {
        case "builtins.bool":
            raw_value_field.type = 'checkbox';
            raw_value_field.checked = !!raw_value;
            raw_value_field.value = "True";
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

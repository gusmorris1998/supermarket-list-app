import { useState } from "react";

function Section(props) {

    const initialItems = props.initialItems;
    const [item, setItem] = useState('')
    const [items, setItems] = useState(initialItems);

    const handleChange = (event) => {
        setItem(event.target.value)
    }

    const handleButtonClick = (item) => () => {
        const newItems = items.concat(item)

        setItems(newItems)
        setItem('');
    };


    return (
        <>
            <h3>{props.heading}</h3>
            <List items={items} setItems={setItems}/>
            <input type="text" value={item} onChange={handleChange}/>
            <Button text="Add" handleClick={handleButtonClick(item)} />
        </>
    )
}

function List(props) {

    const handleButtonDelete = (index) => () => {
        const setItems = props.setItems
        const newItems = props.items.filter((_, i) => i !== index);
        
        setItems(newItems)

    }

    return (
        <ul>
            {props.items.map((item, index) => {
                return (
                    <>
                    <ListItem key={item} item={item} />
                    <Button text="Delete" color="Red" handleClick={handleButtonDelete(index)}/>
                    </>
                )
            })}
        </ul>
    )
}

function ListItem(props) {
    return (
        <li>{props.item}</li>
    )
}

// An example of using default props
function Button({ text = "Click", color = "Blue", fontSize = 12, handleClick }) {
    const buttonStyle = {
        color: color,
        fontSize: fontSize + "px"
    };

    return (
        <button onClick={handleClick} style={buttonStyle}>{text}</button>
    )
}

export default Section;

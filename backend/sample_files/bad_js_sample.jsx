// React component with code quality issues

import React from 'react';

function todoApp(props) {
    var items = [];
    var count = 0;
    
    function handle_click() {
        count = count + 1;
        console.log("Item clicked", count);
    }
    
    function add_item(new_item) {
        items.push(new_item);
        return items;
    }
    
    function process_items(item_list) {
        var result = [];
        for (var i = 0; i < item_list.length; i++) {
            if (item_list[i].status === "completed") {
                if (item_list[i].priority === "high") {
                    if (item_list[i].created_at < Date.now() - 86400000) {
                        result.push({...item_list[i], archived: true});
                    } else {
                        result.push(item_list[i]);
                    }
                } else {
                    result.push(item_list[i]);
                }
            }
        }
        return result;
    }
    
    return (
        <div style={{background: "#f5f5f5", padding: "20px", borderRadius: "5px"}}>
            <h2 style={{color: "#333", fontSize: "24px", marginBottom: "15px"}}>Todo List</h2>
            <ul>
                {props.todos.map((todo, idx) => (
                    <li key={idx} onClick={handle_click.bind(this)} style={{
                        padding: "10px",
                        borderBottom: "1px solid #ddd",
                        cursor: "pointer",
                        backgroundColor: todo.completed ? "#e6ffe6" : "#fff"
                    }}>
                        {todo.text}
                    </li>
                ))}
            </ul>
            <button onClick={() => add_item({text: "New Task", status: "pending"})}>
                Add Item
            </button>
        </div>
    );
} 
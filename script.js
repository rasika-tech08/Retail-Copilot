let products = [];

// Load products from backend
async function loadProducts() {
    try {
        const response = await fetch("/api/products");
        products = await response.json();

        // Display products
        displayProducts(products);

        // Update dashboard statistics
        document.getElementById("totalProducts").textContent = products.length;

        document.getElementById("groceryProducts").textContent =
            products.filter(p => p.category === "Grocery").length;

        document.getElementById("beverageProducts").textContent =
            products.filter(p => p.category === "Beverages").length;

        document.getElementById("personalProducts").textContent =
            products.filter(p => p.category === "Personal Care").length;

    } catch (error) {
        console.error("Error loading products:", error);
    }
}


// Display product cards
function displayProducts(items) {
    const productList = document.getElementById("productList");

    productList.innerHTML = "";

    items.forEach(product => {
        const card = document.createElement("div");

        card.className = "product-card";

        card.innerHTML = `
            <h3>${product.product_name}</h3>
            <p>Category: ${product.category}</p>
            <p>Price: ₹${product.price}</p>
        `;

        productList.appendChild(card);
    });
}


// Ask Copilot
async function askCopilot() {
    const question = document.querySelector("textarea").value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    const answerBox = document.getElementById("answer");

    answerBox.textContent = "Thinking...";

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        answerBox.textContent = data.answer;

    } catch (error) {
        answerBox.textContent = "Something went wrong.";
        console.error(error);
    }
}


// Quick question buttons
function askQuick(question) {
    document.querySelector("textarea").value = question;
    askCopilot();
}


// Load products when page opens
loadProducts();
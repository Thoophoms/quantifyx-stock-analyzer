// Fetch data from Flask API

import React, { useState } from 'react';

// Main app component
function App() {
    // State for stock symbol input by user
    const [symbol, setSymbol] = useState('');

    // State for store fetched price history data
    const [priceData, setPriceData] = useState([]);

    // State for show loading status/errors
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');


    // function to fetch price history data from backend
    const fetchPriceHistory = async () => {
        // show loading sniper/message
        setLoading(true);
        // clear previous errors
        setError('');
        // Clear previous data
        setPriceData([]);

        try {
            // send GET request to Flask backend
            const res = await fetch(`http://127.0.0.1:5000/api/price-history/${symbol}`);
            const data = await res.json();

            // set if statement to catch if backend returns error
            if (data.error) {
                setError(data.error);
            } else {
                // Store the stock history
                setPriceData(data.data);
            }
        } catch (err) {
        setError('Failed to fetch data.');
        }

        // Done loading
        setLoading(false);
    };

    return (
        <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
        <h1>📈 QuantifyX Stock Analyzer</h1>

        {/* Input for stock symbol*/}
        <input
            type="text"
            value={symbol}
            placeholder="Enter symbol (e.g. AAPL)"
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            style={{ marginRight: '1rem', padding: '0.5rem'}}
        />

        {/* Button to trigger API call */}
        <button onClick={fetchPriceHistory} style={{ padding: '0.5rem'}}>
            Fetch Price History
        </button>


        {/* Loading indicator */}
        {loading && <p>Loading...</p>}

        {/* Error display */}
        {error && <p style={{ color: 'red'}}>{error}</p>}

        {/* Price Data list */}
        {priceData.length > 0 && (
            <div style={{ marginTop: '2rem' }}>
                <h3>Price History for {symbol}</h3>
                <ul>
                    {priceData.map((item, index) => (
                        <li key={index}>
                            <strong>{item.date}</strong>: Open {item.open}, Close {item.close}, Volume {item.volume}
                        </li>
                    ))}
                </ul>
            </div>
        )}
    </div>
    );
}

export default App;
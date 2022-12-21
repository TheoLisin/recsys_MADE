import { useState } from "react";

export function getLocalStorageValue<T>(key: string, initialValue: T): T {
    try {
        // Get from local storage by key
        const item = window.localStorage.getItem(key);
        // Parse stored json or if none return initialValue
        return item ? JSON.parse(item) : initialValue;
    } catch (error) {
        // If error also return initialValue
        console.log(error);
        return initialValue;
    }
}

export function setLocalStorageValue<T>(key: string, value: T) {
    try {
        // Save to local storage
        if (typeof window !== "undefined") {
            window.localStorage.setItem(key, JSON.stringify(value));
        }
    } catch (error) {
        // A more advanced implementation would handle the error case
        console.log(error);
    }
}

export function removeFromLocalStorageValue(key: string) {
    try {
        if (typeof window !== "undefined") {
            window.localStorage.removeItem(key);
        }
    } catch (error) {
        // A more advanced implementation would handle the error case
        console.log(error);
    }
}

export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
    // State to store our value
    // Pass initial state function to useState so logic is only executed once
    const [storedValue, setStoredValue] = useState<T>(() => {
        if (typeof window === "undefined") {
            return initialValue;
        }

        return getLocalStorageValue(key, initialValue);
    });

    // Return a wrapped version of useState's setter function that ...
    // ... persists the new value to localStorage.
    const setValue = (value: T) => {
        try {
            // Allow value to be a function so we have same API as useState
            const valueToStore =
                value instanceof Function ? value(storedValue) : value;
            // Save state
            setStoredValue(valueToStore);
            // Save to local storage
            setLocalStorageValue(key, valueToStore);
        } catch (error) {
            // A more advanced implementation would handle the error case
            console.log(error);
        }
    };

    return [storedValue, setValue];
}

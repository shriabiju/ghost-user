import { useState } from "react";

/**
 * "Demo Shop" — a small, deliberately flawed checkout flow used as the
 * app under test. Four intentional UX problems:
 *
 * 1. Low-contrast "Add to Cart" button (easy to miss / read as disabled)
 * 2. A checkout field labeled with internal jargon ("Postal Identifier"
 *    instead of "ZIP code")
 * 3. The real submit button ("Place Order") is visually de-emphasized
 *    compared to a decoy button ("Save for Later")
 * 4. A required "agree to terms" checkbox that silently blocks checkout
 *    if unchecked — no error, no feedback, just nothing happens
 */

const PRODUCT = {
  name: "Wireless Noise-Cancelling Headphones",
  price: "$179.00",
  description:
    "Over-ear headphones with active noise cancellation and 30-hour battery life.",
};

export default function App() {
  const [step, setStep] = useState("product"); // product -> cart -> checkout -> confirmation
  const [form, setForm] = useState({ name: "", address: "", postal: "" });
  const [agreedToTerms, setAgreedToTerms] = useState(false);

  function handlePlaceOrder() {
    // Flaw #4: silent failure — nothing happens if terms aren't agreed to.
    // No error message, no shake, no indication anything went wrong.
    if (!agreedToTerms) return;
    setStep("confirmation");
  }

  return (
    <div className="shop">
      <header className="shop-header">Demo Shop</header>

      {step === "product" && (
        <section className="panel">
          <h1>{PRODUCT.name}</h1>
          <p className="price">{PRODUCT.price}</p>
          <p>{PRODUCT.description}</p>

          {/* Flaw #1: low contrast, looks disabled */}
          <button className="btn-low-contrast" onClick={() => setStep("cart")}>
            Add to Cart
          </button>
        </section>
      )}

      {step === "cart" && (
        <section className="panel">
          <h2>Your Cart</h2>
          <div className="cart-line">
            <span>{PRODUCT.name}</span>
            <span>{PRODUCT.price}</span>
          </div>
          <button className="btn-primary" onClick={() => setStep("checkout")}>
            Checkout
          </button>
        </section>
      )}

      {step === "checkout" && (
        <section className="panel">
          <h2>Checkout</h2>

          <label>
            Full Name
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </label>

          <label>
            Address
            <input
              value={form.address}
              onChange={(e) => setForm({ ...form, address: e.target.value })}
            />
          </label>

          {/* Flaw #2: jargon label instead of "ZIP code" */}
          <label>
            Postal Identifier
            <input
              value={form.postal}
              onChange={(e) => setForm({ ...form, postal: e.target.value })}
            />
          </label>

          {/* Flaw #4: required, unstyled, easy to overlook */}
          <label className="terms-label">
            <input
              type="checkbox"
              checked={agreedToTerms}
              onChange={(e) => setAgreedToTerms(e.target.checked)}
            />
            I agree to the Terms &amp; Conditions
          </label>

          <div className="checkout-actions">
            {/* Flaw #3: decoy button visually stronger than the real submit */}
            <button className="btn-decoy">Save for Later</button>
            <button className="btn-quiet" onClick={handlePlaceOrder}>
              Place Order
            </button>
          </div>
        </section>
      )}

      {step === "confirmation" && (
        <section className="panel">
          <h2>Order Confirmed</h2>
          <p>Thanks, {form.name || "friend"} — your order is on its way.</p>
        </section>
      )}
    </div>
  );
}
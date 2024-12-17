// This is your test secret API key.
const stripe = Stripe("pk_test_51PTl2QRu0n90tW5pw51q19AaBHIoIfcTxK4LO0c7Ka7rMRdF7vXi8zozMIOFcL9GNAMSyMtUflYLgu6z4rhPDKQb00otWiDSq8");

initialize();

// Create a Checkout Session
async function initialize() {
  const fetchClientSecret = async () => {
    const response = await fetch("/create-checkout-session", {
      method: "POST",
    });
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}
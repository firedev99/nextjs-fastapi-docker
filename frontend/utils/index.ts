// handle encrypting text using aes in gcm mode
async function generateEncryptionAES(content: string): Promise<string> {
    if (typeof window === "undefined") return ""
  
    const enc = new TextEncoder()
    // encode the masterkey
    const rawKey = Uint8Array.from(
      atob(process.env.NEXT_PUBLIC_ENCRYPTION_SECRET_KEY as string),
      (c) => c.charCodeAt(0)
    )
    const key = await window.crypto.subtle.importKey(
      "raw",
      rawKey,
      { name: "AES-GCM", length: 256 },
      true,
      ["encrypt", "decrypt"]
    )
    // generate a 12bytes random string
    const iv = window.crypto.getRandomValues(new Uint8Array(12))
  
    // generate encrypted ciphertext w tag
    const ciphertextWithTag = await window.crypto.subtle.encrypt(
      { name: "AES-GCM", iv: iv },
      key,
      enc.encode(content)
    )
  
    const ciphertext = new Uint8Array(ciphertextWithTag.slice(0, -16))
    const tag = new Uint8Array(ciphertextWithTag.slice(-16)) // last 16 bytes as tag
  
    // encrypt everything in a single base64 string
    return Buffer.concat([iv, ciphertext, tag]).toString("base64")
  }


  export const firey = {
    generateEncryption: generateEncryptionAES
  }
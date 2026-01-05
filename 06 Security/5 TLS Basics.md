---
tags:
  - security
---
- Used to guarantee trust between 2 parties during a transaction.
- Ensure the comms between a user and a server are encrypted, and the server is who it says it is.
- You must encrypt the data being transferred, with a key.
- You use the key to encrypt your data (like your username and pw).
- The server also needs the key, so that it will be able to read the message. 
- If the key is also sent over the network, a potential hacker can sniff the encrypted UN and PW, but also the key itself, and use it to decrypt the data. This is known as **symmetric encryption.**
- It's secure, but since **it uses the same key on enc and dec, if someone gets access to the key he can access the data.**
- This is where **asymmetric enc** comes in: 2 different keys, one for sender, one for receiver.
- ![[Pasted image 20251230221330.png]]
- These are **public and private keys, but for the sake of the example, we'll call it a private key, and a public lock**.
- You can think of these as a private key and a public lock. 
- The private key remains securely with the owner, while the public lock can be shared openly. 
- Data encrypted with the public key (aka the lock) can only be decrypted using its corresponding private key, ensuring that intercepted data remains secure.
- An even simpler example with key pairs:
- You gen a public and private key pair, to access a server via SSH:
	Generate your SSH key pair with the following command: :::

	```
	# Generate SSH key pair
	ssh-keygen
	
	
	# Files generated: id_rsa (private key) and id_rsa.pub (public key aka lock)
	```
- You then secure your server by locking down all access to it, except via a door that is locked by **your public lock. ** 
- This is done by adding an entry into the following file. You can review the authorized keys on the server as follows:

```
	cat ~/.ssh/authorized_keys
```

- An example output might appear like:

```
	ssh-rsa AAAAB3NzaC1yc...KhtUBfoTz1BqRV1NThvO0apzEwRQo1mWx user1
```

- Now, the door is locked. Even if anyone tries to break through, no one can get access to it except you with your private key, which is stored safely on your laptop.
- To connect securely to the server using your key pair, use:

```
	ssh -i id_rsa user1@server1
```


- What if you want to use your "lock" on other servers? Well you can copy your lock into other servers as well.
- For additional users who require access, they can generate their own key pairs and have their public keys added to the servers.
- ![[Pasted image 20251230222216.png]]
- Back to the web server example.
- The problem we had with symmetric enc, is that our key to the data had to be sent over the network along with our encrypted data. 
- **What if we could get the key to the server safely?**
- Here’s how the process works for a web server using HTTPS:
1. The server generates a key pair (private and public keys).:
   ![[Pasted image 20251230222703.png]]
2. The user gets the public key from the server upon accessing it via HTTPS. Let's assume a hacker is also sniffing all the traffic, therefore he also gets a copy of the public key:
   ![[Pasted image 20251230222803.png]]
3. The users browser encrypts his symmetric key, using the public key provided by the server. The symmetric key is now secure.
4. The user then sends his enc. data with the key, to the server. The hacker also gets a copy:
   ![[Pasted image 20251230222949.png]]
5. The server uses its own private key to decrypt the incoming message. The hacker, which only has the private key sniffed from the traffic, can't do anything.
6. The client and the server can use the symmetric key to encrypt data and send to each other.

**Asymmetric encryption addresses the issue with symmetric encryption by securely transferring the symmetric key.**

## **Bottom line: Asymmetric enc. uses symmetric keys. The server generates a public key, which he hands to the user upon an https request, the user uses the public key to encrypt his data, and the server uses its own private key (which is paired with the public key as they are created together) to decrypt the encrypted data the user just sent. **



For example, to generate a key pair with OpenSSL for encrypting the symmetric key, you can use:

```
# Generate a private key
openssl genrsa -out my-bank.key 1024


# Extract the public key
openssl rsa -in my-bank.key -pubout > mybank.pem
```


- The hacker thinks about new ways to hack into your account. So he tries phishing (a replica of the real website). He hosts his replica on his own server, with keys and everything. The website even uses HTTPS, therefore the comms are secure from a key standpoint.
- The problem is, obviously, that this whole secure communication is with a hackers server from the get go.
- Modern websites use a **certificate**:
  1. The server generates a key pair (private and public keys).
2. Upon a user's initial HTTPS request, the server sends its public key embedded within a certificate.
3. The client's browser **encrypts a newly generated symmetric key using the server’s public key.**
4. The encrypted symmetric key is sent back to the server.
5. The server **decrypts the symmetric key using its private key.**
6. All subsequent communications are encrypted with this symmetric key.

- A certificate contains essential details that help verify its authenticity:

- Identity of the issuing authority
- The server’s public key
- Domain and other related information

- Below is an example excerpt from a certificate:

```
Certificate:
Data:
  Serial Number: 420327018966204255
  Signature Algorithm: sha256WithRSAEncryption
  Issuer: CN=kubernetes
  Validity
    Not After : Feb  9 13:41:28 2020 GMT
  Subject: CN=my-bank.com
  X509v3 Subject Alternative Name:
    DNS:mybank.com, DNS:i-bank.com,
    DNS:we-bank.com,
  Subject Public Key Info:
    00:b9:b0:55:24:fb:a4:ef:77:73:7c:9b
```

- Anyone can generate a certificate though. It's a one line command. You need an authoritative figure to be responsible on handing out **trusted certificates**, that are proven to be authentic. Someone who can vouch for a websites legitimacy. 
- Browsers rely on Certificate Authorities (CAs) to sign and validate certificates. 
- If the cert is invalid, we get this famous screen:
  ![[Pasted image 20251230224032.png]]
- Renowned CAs, such as Symantec, DigiCert, Komodo, and GlobalSign, use their private keys to sign certificate signing requests (CSRs). 
- But how does the browser know that "Symantec" who signed my incoming certificate is the real one and not just a hacker with a fake name?
- The CA's themselves have public and private keys. The public keys of the CA's are built into the browser - therefore they can validate by decrypting the incoming cert.
- We can even see them in the settings.
- When you generate a CSR for your web server, it is sent to a CA for signing:

```
openssl req -new -key my-bank.key -out my-bank.csr -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=my-bank.com"
```

- Once your details are validated, the CA signs the certificate and sends it back to be installed on your web server. When a user accesses your website, the process is as follows:

1. The server presents the certificate.
2. The browser validates it using pre-installed CA public keys.
3. Upon successful validation, the browser and server establish a secure session using a symmetric key exchanged via asymmetric encryption.


For internal systems, such as corporate payroll applications, organizations may deploy their own private CA and distribute its public key to employee devices.

Key Points Summary

- Asymmetric encryption uses a pair of keys (public and private) to securely exchange symmetric keys.
- SSH access is secured using key pairs.
- Web servers use CA-signed certificates to establish HTTPS connections.
- A Certificate Signing Request (CSR) is generated and sent to a CA for signing.
- Signed certificates, combined with the server’s key pair, secure the communication session. :::

**It is important to note that although both keys in an asymmetric pair can encrypt data, only the complementary key can decrypt it. For instance, data encrypted with your private key can be decrypted by anyone with your public key; therefore, it’s crucial to use the correct key for each operation.**

Regarding file naming conventions, certificates containing public keys typically have extensions such as .crt or .pem (e.g., server.crt, server.pem or client.crt, client.pem), and private key files usually include "key" in the filename or extension (e.g., server.key or server-key.pem).

![The image illustrates public and private keys, showing certificate file types (.crt, .pem) and their roles in encryption.](https://kodekloud.com/kk-media/image/upload/v1752869970/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-TLS-Basics/frame_1160.jpg)



![[Pasted image 20251230225426.png]]
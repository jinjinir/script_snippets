def write_subdomains_to_file(filename: str) -> None:
    with open(filename, 'w') as file:
        for i in range(256):
            subdomain = "0x%02x" % i
            domain = f"{subdomain}.a.hackycorp.com"
            file.write(domain + '\n')

def main() -> None:
    filename = "subdomains.txt"
    write_subdomains_to_file(filename)
    print(f"Subdomains written to {filename}")

if __name__ == "__main__":
    main()
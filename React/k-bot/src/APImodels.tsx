export class VendingProducts {
  products: Kpod[];
}

export class Kpod {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
}

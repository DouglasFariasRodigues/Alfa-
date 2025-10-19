import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { QrCode, Heart, DollarSign, Smartphone } from "lucide-react";

interface QRCodeDonationProps {
  onDonate?: () => void;
}

export const QRCodeDonation: React.FC<QRCodeDonationProps> = ({ onDonate }) => {
  // QR Code simbólico - em produção, seria gerado dinamicamente
  const qrCodeData = "https://igreja.com/doacao/membro-123";

  return (
    <Card className="shadow-card border-green-200 bg-gradient-to-br from-green-50 to-blue-50">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <QrCode className="h-8 w-8 text-green-600" />
        </div>
        <CardTitle className="text-green-800 flex items-center justify-center gap-2">
          <Heart className="h-5 w-5" />
          Doação via QR Code
        </CardTitle>
        <CardDescription className="text-green-700">
          Escaneie o QR Code com seu celular para fazer uma doação
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* QR Code Simbólico */}
        <div className="flex justify-center">
          <div className="relative">
            <div className="h-48 w-48 bg-white border-4 border-green-300 rounded-lg flex items-center justify-center shadow-lg">
              <div className="grid grid-cols-8 gap-1">
                {Array.from({ length: 64 }).map((_, i) => (
                  <div
                    key={i}
                    className={`h-4 w-4 rounded-sm ${
                      Math.random() > 0.5 ? 'bg-green-800' : 'bg-white'
                    }`}
                  />
                ))}
              </div>
            </div>
            <div className="absolute -top-2 -right-2 bg-green-600 text-white rounded-full p-1">
              <Smartphone className="h-4 w-4" />
            </div>
          </div>
        </div>

        {/* Informações da Doação */}
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-white/70 rounded-lg">
            <span className="text-sm font-medium text-green-800">Valor Sugerido:</span>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              R$ 50,00
            </Badge>
          </div>
          
          <div className="flex items-center justify-between p-3 bg-white/70 rounded-lg">
            <span className="text-sm font-medium text-green-800">Destino:</span>
            <span className="text-sm text-green-700">Ofertas da Igreja</span>
          </div>
        </div>

        {/* Instruções */}
        <div className="bg-white/50 p-4 rounded-lg">
          <h4 className="font-medium text-green-800 mb-2">Como doar:</h4>
          <ol className="text-sm text-green-700 space-y-1">
            <li>1. Abra o app do seu banco no celular</li>
            <li>2. Escaneie o QR Code acima</li>
            <li>3. Confirme o valor e finalize a doação</li>
            <li>4. Sua doação será registrada automaticamente</li>
          </ol>
        </div>

        {/* Botão de Ação */}
        <div className="flex gap-2">
          <Button 
            onClick={onDonate}
            className="flex-1 bg-green-600 hover:bg-green-700 text-white"
          >
            <DollarSign className="h-4 w-4 mr-2" />
            Fazer Doação
          </Button>
          <Button variant="outline" className="border-green-300 text-green-700 hover:bg-green-50">
            <QrCode className="h-4 w-4 mr-2" />
            Gerar QR
          </Button>
        </div>

        {/* Aviso */}
        <div className="text-xs text-green-600 text-center">
          <p>💡 Sua doação é registrada automaticamente no sistema</p>
        </div>
      </CardContent>
    </Card>
  );
};

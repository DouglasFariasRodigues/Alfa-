import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { QrCode, DollarSign, Heart, CreditCard, Smartphone } from 'lucide-react';
import { toast } from 'sonner';

interface QRCodeDonationProps {
  onDonate?: (amount: number, method: string) => void;
}

export const QRCodeDonation: React.FC<QRCodeDonationProps> = ({ onDonate }) => {
  const [customAmount, setCustomAmount] = useState('');
  const [selectedMethod, setSelectedMethod] = useState('pix');

  const quickAmounts = [50, 100, 200, 500];

  const handleQuickDonate = (amount: number) => {
    if (onDonate) {
      onDonate(amount, selectedMethod);
    } else {
      toast.success(`Doação de R$ ${amount.toFixed(2)} via ${selectedMethod.toUpperCase()} realizada!`);
    }
  };

  const handleCustomDonate = () => {
    const amount = parseFloat(customAmount);
    if (isNaN(amount) || amount <= 0) {
      toast.error('Por favor, insira um valor válido');
      return;
    }

    if (onDonate) {
      onDonate(amount, selectedMethod);
    } else {
      toast.success(`Doação de R$ ${amount.toFixed(2)} via ${selectedMethod.toUpperCase()} realizada!`);
    }
    setCustomAmount('');
  };

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <QrCode className="h-5 w-5 text-primary" />
          Faça uma Doação
        </CardTitle>
        <CardDescription>
          Contribua para nossa igreja usando QR Code ou transferência
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* QR Code Placeholder */}
        <div className="flex flex-col items-center justify-center p-6 border border-dashed rounded-lg bg-gray-50 dark:bg-gray-900">
          <div className="w-48 h-48 bg-white border-2 border-gray-300 rounded-lg flex items-center justify-center mb-4">
            <QrCode className="h-24 w-24 text-gray-400" />
          </div>
          <p className="text-sm text-muted-foreground text-center">
            Aponte a câmera do seu celular para o QR Code
          </p>
          <p className="text-xs text-muted-foreground text-center mt-1">
            Ou use os valores sugeridos abaixo
          </p>
        </div>

        {/* Método de Pagamento */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Método de Pagamento</Label>
          <div className="flex gap-2">
            <Button
              variant={selectedMethod === 'pix' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedMethod('pix')}
              className="flex-1"
            >
              <Smartphone className="h-4 w-4 mr-2" />
              PIX
            </Button>
            <Button
              variant={selectedMethod === 'cartao' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedMethod('cartao')}
              className="flex-1"
            >
              <CreditCard className="h-4 w-4 mr-2" />
              Cartão
            </Button>
          </div>
        </div>

        {/* Valores Rápidos */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Valores Sugeridos</Label>
          <div className="grid grid-cols-2 gap-2">
            {quickAmounts.map((amount) => (
              <Button
                key={amount}
                variant="outline"
                onClick={() => handleQuickDonate(amount)}
                className="h-12"
              >
                <DollarSign className="h-4 w-4 mr-2" />
                R$ {amount.toFixed(2)}
              </Button>
            ))}
          </div>
        </div>

        {/* Valor Personalizado */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Valor Personalizado</Label>
          <div className="flex gap-2">
            <div className="flex-1">
              <Input
                type="number"
                placeholder="Digite o valor"
                value={customAmount}
                onChange={(e) => setCustomAmount(e.target.value)}
                min="0.01"
                step="0.01"
              />
            </div>
            <Button
              onClick={handleCustomDonate}
              disabled={!customAmount || parseFloat(customAmount) <= 0}
            >
              <Heart className="h-4 w-4 mr-2" />
              Doar
            </Button>
          </div>
        </div>

        {/* Informações Adicionais */}
        <div className="text-center space-y-2">
          <p className="text-sm text-muted-foreground">
            Sua generosidade abençoa nossa comunidade!
          </p>
          <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
            <Heart className="h-3 w-3 text-red-500" />
            <span>Doações são seguras e criptografadas</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

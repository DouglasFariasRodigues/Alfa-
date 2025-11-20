import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Calendar, MapPin, Users, Clock, MessageCircle, Send, Check, X } from "lucide-react";
import { auth } from "@/lib/auth";
import { useToast } from "@/hooks/use-toast";

const events = [
  {
    id: 1,
    title: "Reunião de Oração",
    description: "Reunião semanal de oração e intercessão pela comunidade",
    date: "2024-01-15",
    time: "19:00",
    location: "Salão Principal",
    attendees: 45,
    maxAttendees: 50,
    status: "Confirmado",
    jaConfirmei: false,
    comments: [
      {
        id: 1,
        author: "Maria Santos",
        content: "Estou ansiosa para participar!",
        time: "2 horas atrás"
      },
      {
        id: 2,
        author: "João Silva",
        content: "Será uma bênção estar juntos em oração.",
        time: "1 hora atrás"
      }
    ]
  },
  {
    id: 2,
    title: "Culto de Domingo",
    description: "Culto dominical com mensagem especial",
    date: "2024-01-14",
    time: "10:00",
    location: "Templo Central",
    attendees: 120,
    maxAttendees: 150,
    status: "Confirmado",
    jaConfirmei: false,
    comments: [
      {
        id: 1,
        author: "Ana Costa",
        content: "Ansiosa pela mensagem de hoje!",
        time: "30 minutos atrás"
      }
    ]
  },
  {
    id: 3,
    title: "Estudo Bíblico",
    description: "Estudo sobre o livro de Romanos",
    date: "2024-01-16",
    time: "20:00",
    location: "Sala de Estudos",
    attendees: 15,
    maxAttendees: 25,
    status: "Confirmado",
    jaConfirmei: false,
    comments: []
  }
];

export default function MemberEvents() {
  const [selectedEvent, setSelectedEvent] = useState(events[0]);
  const [eventsState, setEventsState] = useState(events);
  const [newComment, setNewComment] = useState("");
  const { toast } = useToast();
  const userEmail = auth.getUserEmail();

  // Load confirmed events from localStorage
  useEffect(() => {
    const confirmedEvents = JSON.parse(localStorage.getItem(`confirmedEvents_${userEmail}`) || '[]');
    setEventsState(prev => prev.map(event => ({
      ...event,
      jaConfirmei: confirmedEvents.includes(event.id)
    })));
    setSelectedEvent(prev => {
      const updated = eventsState.find(e => e.id === prev.id);
      return updated || prev;
    });
  }, [userEmail, eventsState]);

  // Save confirmed events to localStorage
  const saveConfirmedEvents = (confirmedIds: number[]) => {
    localStorage.setItem(`confirmedEvents_${userEmail}`, JSON.stringify(confirmedIds));
  };

  const handleComment = () => {
    if (newComment.trim()) {
      // In a real app, this would send to backend
      console.log("New comment:", newComment);
      setNewComment("");
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Eventos</h1>
        <p className="text-muted-foreground">
          Participe dos eventos da nossa comunidade
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Events List */}
        <div className="lg:col-span-1 space-y-4">
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Próximos Eventos</CardTitle>
              <CardDescription>
                Eventos programados
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {events.map((event) => (
                <div
                  key={event.id}
                  className={`p-3 rounded-lg cursor-pointer transition-smooth hover:bg-accent/50 ${
                    selectedEvent.id === event.id ? 'bg-accent border-primary' : ''
                  }`}
                  onClick={() => setSelectedEvent(event)}
                >
                  <div className="flex items-start space-x-3">
                    <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Calendar className="h-5 w-5 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{event.title}</p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(event.date).toLocaleDateString('pt-BR')} às {event.time}
                      </p>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge variant="outline" className="text-xs">
                          {event.attendees}/{event.maxAttendees}
                        </Badge>
                        <Badge
                          variant={event.status === 'Confirmado' ? 'default' : 'secondary'}
                          className="text-xs"
                        >
                          {event.status}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Event Details */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="shadow-card">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-xl">{selectedEvent.title}</CardTitle>
                  <CardDescription className="mt-2">
                    {selectedEvent.description}
                  </CardDescription>
                </div>
                <Badge
                  variant={selectedEvent.status === 'Confirmado' ? 'default' : 'secondary'}
                  className="gradient-primary text-white"
                >
                  {selectedEvent.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="flex items-center space-x-3">
                  <Calendar className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Data e Hora</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(selectedEvent.date).toLocaleDateString('pt-BR')} às {selectedEvent.time}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <MapPin className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Local</p>
                    <p className="text-sm text-muted-foreground">{selectedEvent.location}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Users className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Participantes</p>
                    <p className="text-sm text-muted-foreground">
                      {selectedEvent.attendees} de {selectedEvent.maxAttendees} confirmados
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Clock className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Status</p>
                    <p className="text-sm text-muted-foreground">{selectedEvent.status}</p>
                  </div>
                </div>
              </div>

              <div className="pt-4">
                <Button
                  variant={selectedEvent.jaConfirmei ? "destructive" : "default"}
                  className={selectedEvent.jaConfirmei ? "" : "gradient-primary text-white shadow-elegant hover:opacity-90"}
                  onClick={() => confirmarPresenca(selectedEvent.id)}
                >
                  {selectedEvent.jaConfirmei ? (
                    <>
                      <X className="h-4 w-4 mr-2" />
                      Cancelar Presença
                    </>
                  ) : (
                    <>
                      <Check className="h-4 w-4 mr-2" />
                      Confirmar Presença
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Comments Section */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageCircle className="h-5 w-5" />
                <span>Comentários</span>
              </CardTitle>
              <CardDescription>
                Compartilhe seus pensamentos sobre este evento
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Existing Comments */}
              <div className="space-y-4">
                {selectedEvent.comments.map((comment) => (
                  <div key={comment.id} className="flex items-start space-x-3 p-3 rounded-lg bg-accent/30">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src="" alt={comment.author} />
                      <AvatarFallback className="gradient-primary text-white text-xs">
                        {comment.author.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <p className="text-sm font-medium">{comment.author}</p>
                        <p className="text-xs text-muted-foreground">{comment.time}</p>
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">{comment.content}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* New Comment Input */}
              <div className="flex items-end space-x-2 pt-4 border-t">
                <div className="flex-1">
                  <Input
                    placeholder="Escreva um comentário..."
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleComment()}
                  />
                </div>
                <Button
                  onClick={handleComment}
                  size="sm"
                  className="gradient-primary text-white"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

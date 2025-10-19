import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'

export interface Cargo {
  id: number
  nome: string
  descricao?: string
  criado_por?: number
  data_criacao: string
  pode_fazer_postagens: boolean
  pode_registrar_dizimos: boolean
  pode_registrar_ofertas: boolean
}

export interface CargoCreate {
  nome: string
  descricao?: string
  pode_fazer_postagens?: boolean
  pode_registrar_dizimos?: boolean
  pode_registrar_ofertas?: boolean
}

export interface CargoUpdate extends Partial<CargoCreate> {
  id: number
}

export interface CargoFilters {
  search?: string
  pode_fazer_postagens?: boolean
  pode_registrar_dizimos?: boolean
  pode_registrar_ofertas?: boolean
}

// Hook para listar cargos
export const useCargos = (filters?: CargoFilters) => {
  return useQuery({
    queryKey: ['cargos', filters],
    queryFn: async () => {
      return await apiClient.getCargos(filters)
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  })
}

// Hook para obter um cargo específico
export const useCargo = (id: number) => {
  return useQuery({
    queryKey: ['cargo', id],
    queryFn: async () => {
      return await apiClient.getCargo(id)
    },
    enabled: !!id,
  })
}

// Hook para criar cargo
export const useCreateCargo = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data: CargoCreate) => {
      return await apiClient.createCargo(data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cargos'] })
    },
  })
}

// Hook para atualizar cargo
export const useUpdateCargo = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...data }: CargoUpdate) => {
      return await apiClient.updateCargo(id, data)
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['cargos'] })
      queryClient.invalidateQueries({ queryKey: ['cargo', data.id] })
    },
  })
}

// Hook para deletar cargo
export const useDeleteCargo = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.deleteCargo(id)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cargos'] })
    },
  })
}

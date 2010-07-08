package org.globus.workspace.spotinstances;

import java.util.Collection;
import java.util.LinkedList;

public class MaximizeProfitPricingModel extends AbstractPricingModel {

    
    @Override
    public Double getNextPriceImpl(Integer totalReservedResources, Collection<SIRequest> requests, Double currentPrice) {
                
        LinkedList<Double> priceCandidates = getOrderedPriceCandidates(requests);
        
        Double highestProfitPrice = PricingModelConstants.NEGATIVE_INFINITY;
        Double highestProfit = PricingModelConstants.NEGATIVE_INFINITY;
        
        for (Double priceCandidate : priceCandidates) {
            Double profit = getProfit(priceCandidate, totalReservedResources, requests);
            if(profit > highestProfit){
                highestProfit = profit;
                highestProfitPrice = priceCandidate;
            }
        }
        
        if(highestProfitPrice == PricingModelConstants.NEGATIVE_INFINITY){
            Double highestPrice = priceCandidates.getLast();
            return highestPrice+1;
        }
        
        return highestProfitPrice;
    }


    private static Double getProfit(Double priceCandidate, Integer availableResources, Collection<SIRequest> allRequests){
        
        Collection<SIRequest> priorityOffers = SIRequestUtils.getRequestsAbovePrice(priceCandidate, allRequests);
        Collection<SIRequest> limitOffers = SIRequestUtils.getRequestsEqualPrice(priceCandidate, allRequests);
        
        Collection<SIRequest> eligibleOffers = union(priorityOffers, limitOffers);
        
        Double priorityUtilization = getUtilization(priorityOffers, availableResources);
        
        if(!priorityOffers.isEmpty() && priorityUtilization >= 1.0){
            return PricingModelConstants.NEGATIVE_INFINITY;
        }
        
        return getProfitFromEligibleOffers(eligibleOffers, priceCandidate);
    }

    private static Double getProfitFromEligibleOffers(Collection<SIRequest> eligibleOffers, Double priceCandidate) {
        
        Double totalProfit = 0.0;
        
        for (SIRequest siRequest : eligibleOffers) {
            totalProfit += siRequest.getNeededInstances()*priceCandidate;
        }
        
        return totalProfit;
    }

    private static Collection<SIRequest> union(
            Collection<SIRequest> priorityOffers,
            Collection<SIRequest> limitOffers) {
        
        LinkedList<SIRequest> union = new LinkedList<SIRequest>(priorityOffers);
        union.addAll(limitOffers);
        
        return union;
    }

    private static Double getUtilization(Collection<SIRequest> bids, Integer offeredResources){
        
        Double demand = 0.0;
        
        for (SIRequest siRequest : bids) {
            demand += siRequest.getNeededInstances();
        }
        
        return demand/offeredResources;
    }

}
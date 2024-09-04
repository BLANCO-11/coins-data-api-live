package com.rev.demo.Service;

import com.rev.demo.Repository.CryptocurrencyRepository;
import com.rev.demo.Model.Cryptocurrency;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class CryptocurrencyService {
    private final CryptocurrencyRepository repository;

    public CryptocurrencyService(CryptocurrencyRepository repo){
        this.repository = repo;
    }

    public List<Map<String, Map<String, Object>>> getAllCryptocurrency() {
        List<Cryptocurrency> cryptocurrencies = repository.findAll();

        // Transform the list into the desired JSON format
        return cryptocurrencies.stream()
            .map(crypto -> {
                Map<String, Object> cryptoMap = new HashMap<>();
                cryptoMap.put("id", crypto.getId());
                cryptoMap.put("name", crypto.getName());
                cryptoMap.put("symbol", crypto.getSymbol());
                cryptoMap.put("price", crypto.getPrice());
                cryptoMap.put("priceChange", crypto.getPriceChange());
                cryptoMap.put("volume", crypto.getVolume());
                cryptoMap.put("volChange", crypto.getVolChange());
                cryptoMap.put("volRank", crypto.getVolRank());
                cryptoMap.put("circulatingSupply", crypto.getCirculatingSupply());
                cryptoMap.put("totalSupply", crypto.getTotalSupply());
                cryptoMap.put("maxSupply", crypto.getTotalSupply());
                cryptoMap.put("dilutedMarketCap", crypto.getDilutedMarketCap());
                cryptoMap.put("contracts", crypto.getContracts());
                cryptoMap.put("socials", crypto.getSocials());
                cryptoMap.put("officialLinks", crypto.getOfficialLinks());
                cryptoMap.put("lastUpdate", crypto.getLastUpdate());

                Map<String, Map<String, Object>> resultMap = new HashMap<>();
                resultMap.put(crypto.getName().toLowerCase(), cryptoMap);

                return resultMap;
            })
            .collect(Collectors.toList());
    }

    public Cryptocurrency savCryptocurrency(Cryptocurrency crypto){
        return repository.save(crypto);
    }

    public Optional<Cryptocurrency> getCrptocurrencyByName(String name){
        return repository.findByName(name);
    }

}

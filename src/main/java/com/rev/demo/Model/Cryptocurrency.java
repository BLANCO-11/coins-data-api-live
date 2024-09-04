package com.rev.demo.Model;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.sql.Timestamp;
import java.time.Instant;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "cryptocurrency")
public class Cryptocurrency {
    
    @Id
    private String id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String symbol;

    @Column(precision = 18, scale = 4)
    private BigDecimal price;

    @Column(precision = 18, scale = 2)
    private BigDecimal price_change;

    @Column(precision = 18, scale = 2)
    private BigDecimal volume;

    @Column(precision = 18, scale = 2)
    private BigDecimal vol_change;

    private int vol_rank;

    private BigInteger circulating_supply;

    private BigInteger total_supply;

    private BigInteger max_supply;

    @Column(precision = 18, scale = 2)
    private BigDecimal diluted_market_cap;

    @Column(columnDefinition = "jsonb")
    private String contracts;

    @Column(columnDefinition = "jsonb")
    private String socials;
    
    @Column(columnDefinition = "jsonb")
    private String official_links;

    @Column(name="last_update")
    private Timestamp lastUpdate;

    public Cryptocurrency(){
        this.lastUpdate = Timestamp.from(Instant.now());
    }

    @Override
    public String toString() {
        return "Cryptocurrency{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", symbol='" + symbol + '\'' +
                ", price=" + price +
                ", priceChange=" + price_change +
                ", volume=" + volume +
                ", volChange=" + vol_change +
                ", volRank=" + vol_rank +
                ", circulatingSupply=" + circulating_supply +
                ", totalSupply=" + total_supply +
                ", maxSupply=" + max_supply +
                ", dilutedMarketCap=" + diluted_market_cap +
                ", contracts='" + contracts + '\'' +
                ", socials='" + socials + '\'' +
                ", officialLinks='" + official_links + '\'' +
                ", lastUpdate=" + lastUpdate +
                '}';
    }

    private static final ObjectMapper objectMapper = new ObjectMapper();

    public String getId(){
        return this.id;
    }
    public String getName() {
        return this.name;
    }
    public String getSymbol(){
        return this.symbol;
    }
    public Object getPrice(){
        return this.price;
    }
    public Object getPriceChange() {
        return this.price_change;
    }
    public Object getVolume() {
        return this.volume;
    }
    public Object getVolChange() {
        return this.vol_change;
    }

    public Object getCirculatingSupply() {
        return this.circulating_supply;
    }

    public Object getVolRank() {
        return this.vol_rank;
    }

    public Object getTotalSupply() {
        return this.total_supply;
    }

    public Object getDilutedMarketCap() {
        return this.diluted_market_cap;
    }

    public JsonNode getContracts() {
        return parseJson(contracts);
    }

    public JsonNode getSocials() {
        return parseJson(socials);
    }

    public JsonNode getOfficialLinks() {
        return parseJson(official_links);
    }

    private JsonNode parseJson(String jsonString) {
        try {
            return objectMapper.readTree(jsonString);
        } catch (Exception e) {
            // Log and handle the error as needed
            e.printStackTrace();
            return null; // or return an empty JsonNode, based on your needs
        }
    }

    public Object getLastUpdate() {
        return this.lastUpdate;
    }
}
